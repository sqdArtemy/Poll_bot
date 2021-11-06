from django import forms
from django.contrib import admin

from .models import AnsweredUsers, Answers, Language, Profile, Question, RightAnswers
from .forms import LanguageForm, ProfileForm, QuestionForm

class InlineAnswers(admin.StackedInline):
    model = Answers

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id',
    'name',
    'phone',
    'language',
    'wallet',
    'chosen_ques',
    'chosen_ans',
    'state')
    form = ProfileForm

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name','greeting', 
        'profile',
        'post',
        'wallet',
        'ans_ques',
        'question',
        'balance',
        'lang_choose',
        'correct',
        'accepted',
        'inact_ques',
        'ansd_ques',
        'ent_name',
        'ent_phone',
        'send_num')
    form = LanguageForm

@admin.register(Question)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'right_choice', 'number', 'prize', 'status','answered')
    form = QuestionForm

    inlines = [InlineAnswers]

@admin.register(AnsweredUsers)
class AnsweredQuestionAdmin(admin.ModelAdmin):
    list_display = ('question','user_id','answer')

@admin.register(RightAnswers)
class RightAnswersAdmin(admin.ModelAdmin):
    list_display = ('question','user_id', 'name','phone', 'answer','number', 'send_money')
    list_editable = ('send_money'),
    list_filter = (('question'),)