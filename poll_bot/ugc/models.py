from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import PROTECT
from django.db.models.fields import TextField
import django.utils.timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from telegram.update import Update
from poll_bot.settings import TOKEN
from telegram import Bot
# Create your models here.


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Telegram ID',
        unique=True,
    )
    language = models.TextField(
        verbose_name='Chosen language',
        default='RU🇷🇺'
    )
    wallet = models.FloatField(
        verbose_name='User`s money',
        default=0
    )
    chosen_ques = models.TextField(
        verbose_name='Chosen question',
        default=0,
    )
    chosen_ans = models.TextField(
        verbose_name='Chosen answer to the question',
        default=0
    )
    name = models.TextField(
        verbose_name='Name of the user'
    )
    phone = models.TextField(
        verbose_name='Phone number'
    )
    state = models.TextField(
        verbose_name='Where is user',
        default='start'
    )

    def __str__(self):
        return f'User #{self.external_id}'

    class Meta:
        verbose_name = 'Users profile'


class Language(models.Model):
    name = models.TextField(
        verbose_name='Language',
        unique=True,
    )
    greeting = models.TextField(
        verbose_name='Greeting',
    )
    profile = models.TextField(
        verbose_name='Profile'
    )
    post = models.TextField(
        verbose_name='Post'
    )
    wallet = models.TextField(
        verbose_name='My Wallet'
    )
    ans_ques = models.TextField(
        verbose_name='Answer to question'
    )
    question = models.TextField(
        verbose_name='Question'
    )
    lang_choose = models.TextField(
        verbose_name='Chosen language'
    )
    balance = models.TextField(
        verbose_name='Your balance:'
    )
    correct = models.TextField(
        verbose_name='Correct answer!'
    )
    accepted = models.TextField(
        verbose_name='Answer is accepted'
    )
    inact_ques = models.TextField(
        verbose_name='Question in inactive!',
    )
    ansd_ques = models.TextField(
        verbose_name='Question is already answered'
    )
    ent_name = models.TextField(
        verbose_name='Enter your name'
    )
    ent_phone = models.TextField(
        verbose_name='Enter your phone'
    )
    send_num = models.TextField(
        verbose_name='Send number'
    )

    class Meta:
        verbose_name = 'Language'


class Question(models.Model):
    name = models.TextField(
        verbose_name='Question'
    )
    right_choice = models.ForeignKey(
        'Answers',
        on_delete=models.PROTECT
    )
    number = models.PositiveIntegerField(
        verbose_name='Number of the qustion'
    )
    winners_number = models.PositiveIntegerField(
        verbose_name='Number of winners'
    )
    prize = models.FloatField(
        verbose_name='Prize'
    )
    time = models.DateTimeField(
        verbose_name='Available at this time:',
        default=django.utils.timezone.now
    )
    status = models.TextField(
        verbose_name='Question status',
        default='Inactive'
    )
    answered = models.PositiveIntegerField(
        verbose_name='Users answered',
        default=0
    )

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = 'Question'


class Answers(models.Model):
    name = models.TextField(
        verbose_name='Text of the answer'
    )
    number = models.PositiveIntegerField(
        verbose_name='Number of the answer'
    )
    of_question = models.ForeignKey(
        'Question',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Answers to the question'


class AnsweredUsers(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=models.PROTECT
    )
    user_id = models.PositiveIntegerField(
        verbose_name='User`s ID',
    )
    answer = models.ForeignKey(
        'Answers',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Answers to questions by user'


class RightAnswers(models.Model):
    question = models.ForeignKey(
        'Question',
        on_delete=PROTECT
    )
    user_id = models.PositiveIntegerField(
        verbose_name='User`s ID'
    )
    name = models.TextField(
        verbose_name='User`s name'
    )
    phone = models.TextField(
        verbose_name='User`s phone'
    )
    answer = models.ForeignKey(
        'Answers',
        on_delete=PROTECT,
    )
    number = models.PositiveIntegerField(
        verbose_name='Position'
    )
    send_money = models.BooleanField(
        verbose_name='Send Prize',
        default=False
    )

    class Meta:
        verbose_name = 'Right answers by user'


@receiver(post_save, sender=AnsweredUsers)
def counter(instance, **kwargs):

    user = Profile.objects.filter(external_id=instance.user_id).get()

    AnsweredUsers.objects.filter(
        question=instance.question, answer=instance.question.right_choice).count()

    if instance.question.right_choice == instance.answer:
        RightAnswers.objects.create(
            question=instance.question,
            user_id=instance.user_id,
            name=user.name,
            phone=user.phone,
            answer=instance.question.right_choice,
            number=AnsweredUsers.objects.filter(
                question=instance.question, answer=instance.question.right_choice).count()
        )


@receiver(post_save, sender=Profile)
def name_change(instance, **kwargs):
    def upd(data):
        Profile.objects.filter(
            external_id=instance.external_id).update(state=data)

    if instance.state == 'name':
        upd('phone')
    elif instance.state == 'phone':
        upd('menu')


@receiver(post_save, sender=RightAnswers)
def send_prize(instance, **kwargs):
    user = Profile.objects.filter(external_id=instance.user_id).get()
    wallet = user.wallet

    if instance.send_money == True:
        Profile.objects.filter(external_id=instance.user_id).update(
            wallet=wallet + instance.question.prize)

        bot = Bot(
            token=TOKEN,
        )

        lang = Language.objects.filter(name=user.language).get()
        field_obj = Language._meta.get_field('correct')
        phrase = getattr(lang, field_obj.attname)

        try:
            bot.send_message(
                chat_id=instance.user_id,
                text=phrase
            )
        except:
            pass
