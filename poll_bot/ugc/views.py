from django.http import JsonResponse
from poll_bot.settings import TOKEN
from poll_bot.settings import TOKEN
from telegram import *
from telegram.ext import *
import os
from .management.commands.bot import callback_handler, contact_callback, message_handler, start
from rest_framework.views import APIView


class Test(APIView):

    # this function is for setting webhook
    def get(self, request, *args, **options):
        PORT = int(os.environ.get('PORT', '8000'))
        bot = Bot(token=TOKEN)
        url = "https://2695-213-230-127-84.ngrok.io/"  # link for your web-app

        bot.setWebhook(url + 'poll_bot/')

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url=(url+'poll_bot/'))

    def post(self, request, *args, **options):
        bot = Bot(token=TOKEN)
        dispatcher = Dispatcher(bot, None, workers=6)

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(
            Filters.text, callback=message_handler))
        dispatcher.add_handler(CallbackQueryHandler(callback=callback_handler))
        dispatcher.add_handler(MessageHandler(
            Filters.contact, callback=contact_callback))

        dispatcher.process_update(Update.de_json(request.data, bot))
        return JsonResponse({"ok": "POST request processed"})
