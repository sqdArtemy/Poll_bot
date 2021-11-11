from django import views
from django.http import response
from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views import View
from telegram import chat

from poll_bot.settings import TOKEN

from django.core.management.base import BaseCommand
from poll_bot.settings import TOKEN
from telegram import *
from telegram.ext import *
import os
from .management.commands.bot import Command, callback_handler, contact_callback, message_handler, start
from ugc.models import Language, Profile, Question, Answers, AnsweredUsers
from rest_framework.views import APIView


class Test(APIView):
    def post(self, request, *args, **options):

        PORT = int(os.environ.get('PORT', '8000'))

        bot = Bot(token = TOKEN)
   
        dispatcher = Dispatcher(bot, None, workers=6)


        # update = Update.de_json(request.get_json(force=True), bot,use_context = True,)

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, callback=message_handler))
        dispatcher.add_handler(CallbackQueryHandler(callback=callback_handler))
        dispatcher.add_handler(MessageHandler(Filters.contact, callback=contact_callback))

        dispatcher.process_update( Update.de_json(request.data, bot))
        return JsonResponse({"ok": "POST request processed"})
