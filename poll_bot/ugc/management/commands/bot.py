from django.core.management.base import BaseCommand
from poll_bot.settings import TOKEN
from telegram import *
from telegram.ext import *
import os
from ugc.models import Language, Profile, Question, Answers, AnsweredUsers

# getting current user`s id
def get_id(update: Update):
    chat_id = update.effective_message.chat_id
    return chat_id

# getting needed item from database
def get_item(update: Update, id, item, type):
    user = type.objects.filter(external_id = id).get()
    field_object = type._meta.get_field(str(item))
    choosen_item = getattr(user, field_object.attname)
    
    return choosen_item

# getting words in selected language 
def get_phrase(update: Update, lang, field):
    lang = Language.objects.filter(name = lang).get()
    field_obj = Language._meta.get_field(str(field))
    phrase = getattr(lang, field_obj.attname)

    return(phrase)

# creating buttons for keyboard
def buttons(update: Update, type):
    buttons = []
    chat_id = get_id(update)
    items_db = type.objects.all()

    for item in items_db:
        buttons.append(KeyboardButton(text = str(item.name)))

    update.message.reply_text(
            text = 'test',
            reply_markup= ReplyKeyboardMarkup(
                keyboard=[buttons,],
                resize_keyboard=True
            )  
        )

#function which ables to choose language
def start(update, context):
    chat_id = get_id(update)
    Profile.objects.filter(external_id = chat_id).update(state = 'start')

    #creates new user in the database
    p, _ = Profile.objects.get_or_create(
            external_id = chat_id,
        )

    update.message.reply_text(
        text = get_phrase(update, get_item(update, chat_id, 'language', Profile), 'greeting'),
        reply_markup = inline_keyboard(update, Language),
        )

# creating inline keyboard for the questions and answers
def inline_keyboard(update: Update, type):
    chat_id = get_id(update)
    BTNS = {}
    keyboard = []

    items_set = type.objects.all()

    for item in items_set:

        if type == Answers or type == Language:
            text = str(item.name)
        else:
            text = int(item.number)

        if type == Answers and str(get_item(update, chat_id, 'chosen_ques', Profile)) == str(item.of_question):
            BTNS[item.number] = text
            keyboard.append([InlineKeyboardButton(BTNS[item.number], callback_data=text)])
        elif type == Question:
            BTNS[item.number] = text
            keyboard.append([InlineKeyboardButton(BTNS[item.number], callback_data=text)])
        elif type == Language:
            BTNS[item.name] = text
            keyboard.append([InlineKeyboardButton(BTNS[item.name], callback_data=text)]) 

    return InlineKeyboardMarkup(keyboard)

#checks if particular language selected and creates menu
def menu(update: Update):
    chat_id = get_id(update)
    wallet = get_phrase(update, language(update), 'wallet')
    question = get_phrase(update, language(update), 'ans_ques')
    
    if get_item(update,chat_id, 'state', Profile) == 'menu':
        bot = Bot(token = TOKEN)
        bot.send_message(
            chat_id = chat_id,
            text = get_phrase(update, language(update), 'post'),
            reply_markup = ReplyKeyboardMarkup(
                keyboard= [[wallet, question]],
                    resize_keyboard= True
                )
            )
    elif get_item(update,chat_id, 'state', Profile) == 'phone':
        bot = Bot(token = TOKEN)
        bot.send_message(
            chat_id = chat_id,
            text = get_phrase(update, language(update), 'ent_phone'),
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text= get_phrase(update, language(update),'send_num'), request_contact=True)]],resize_keyboard=True)
        )
    else:
        Profile.objects.filter(external_id = chat_id).update(state = 'name')
        ask_name(update, chat_id)

#asking user`s name
def ask_name(update: Update, chat_id):
    bot = Bot(token = TOKEN)
    bot.send_message(
        chat_id,            
        text = get_phrase(update, language(update), 'ent_name'),
        reply_markup = ReplyKeyboardRemove()
    )

# gives language selected by user
def language(update:Update):
    chat_id = get_id(update)
    return get_item(update, chat_id, 'language', Profile)

#callback handler for inline keyboard
def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = get_id(update)

    # when user selected question 
    if len(data) == 1:
        Profile.objects.filter(external_id = chat_id).update(chosen_ques = data)
        question = Question.objects.filter(number = data).get()

        if question.status == 'Active':
            if(not AnsweredUsers.objects.filter(user_id = chat_id, question = question).exists()):
                query.edit_message_text(
                    text=question.name,
                    reply_markup=inline_keyboard(update, Answers)
                    )
            else:
                query.answer(get_phrase(update,language(update),'ansd_ques'))
        else:
            query.answer(get_phrase(update, language(update), 'inact_ques'))
    
    # when user selected language
    elif data == 'UZ🇺🇿' or data == 'RU🇷🇺':
        Profile.objects.filter(external_id = chat_id).update(language = data)

        query.edit_message_text(
            text = get_phrase(update, language(update), 'lang_choose'),
        )

        menu(update)

    else:
        Profile.objects.filter(external_id = chat_id).update(chosen_ans = data)
        answer = Answers.objects.filter(name = data).get()
        query.edit_message_text(
            text= get_phrase(update, language(update), 'accepted'),
            )
        create_item(update,chat_id,answer.of_question,answer)


def create_item(update: Update, user_id, question, answer):
    AnsweredUsers.objects.create(
        user_id = user_id,
        question = question,
        answer = answer
    )

# checks every message
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = get_id(update)

    def language(update):
        return get_item(update, chat_id, 'language', Profile)

    wallet = get_phrase(update, language(update), 'wallet')
    ans_ques = get_phrase(update, language(update), 'ans_ques')

    # creates or updates the user
    p, _ = Profile.objects.get_or_create(
            external_id = chat_id,
        )

    state = get_item(update, chat_id, 'state', Profile)

    #save user`s` name in DB
    if state == 'name':
       profile =  Profile.objects.filter(external_id = chat_id).last()
       profile.name = update.message.text
       profile.save()

       menu(update)
    
    elif state == 'phone':
        profile =  Profile.objects.filter(external_id = chat_id).last()
        profile.phone = update.message.text
        profile.save()

        menu(update)

    # info about profile`s balance
    if text == wallet:
        phrase = (str(get_phrase(update, language(update), 'balance'))+'  '+str(get_item(update, chat_id, 'wallet', Profile)))
        update.message.reply_text(
            text = phrase
        )

    if text == ans_ques:
        update.message.reply_text(
            text = get_phrase(update, language(update), 'question'),
            reply_markup = inline_keyboard(update, Question)
        )

# writes user`s phone number into DB
def contact_callback(update: Update, context: CallbackContext):
    contact = update.effective_message.contact
    phone = contact.phone_number

    profile =  Profile.objects.filter(external_id = get_id(update)).last()
    profile.phone = phone
    profile.save()
    menu(update)

# class wich adds bot as a django command
class Command(BaseCommand):
    help = 'Poll_bot'
    
    def handle(self, *args, **options):

        PORT = int(os.environ.get('PORT', '5000'))

        global bot
        bot = Bot(token = TOKEN)
        url = "https://6ac3-213-230-127-84.ngrok.io/"

        bot.setWebhook(url + TOKEN)

        updater = Updater(
            bot = bot,
            use_context = True,
        )
        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, callback=message_handler, run_async=True))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=callback_handler, run_async = True))
        updater.dispatcher.add_handler(MessageHandler(Filters.contact, callback=contact_callback))

        # updater.start_polling()
        # updater.idle()
        updater.start_webhook(listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=(url + TOKEN))
        updater.idle()