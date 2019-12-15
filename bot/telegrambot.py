from bot.models import Member
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from django_telegrambot.apps import DjangoTelegramBot
from .Handler import *
import logging
from uuid import uuid4

logger = logging.getLogger(__name__)

head = lambda func: \
    lambda bot, update, args=[]: \
        func(bot, update,
             Member.objects.get_or_create(tel=update.message.chat_id,
                                          defaults={"username": str(uuid4())[:8]})[0],
             *args)
call_back = lambda func: \
    lambda bot, update: \
        func(bot, update.callback_query, Member.objects.get_or_create(tel=update.callback_query.from_user.id

                                                                      )[0])


def error(bot, update, error, *args):
    logger.warn('Update "%s' % error)


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", head(on_start), pass_args=True))
    dp.add_handler(CommandHandler("help", head(on_help)))
    dp.add_handler(MessageHandler(Filters.text, head(message_handler)))
    dp.add_handler(MessageHandler(Filters.photo, head(photo_handler)))
    dp.add_handler(MessageHandler(Filters.voice, head(photo_handler)))
    dp.add_handler(MessageHandler(Filters.video, head(photo_handler)))
    dp.add_handler(MessageHandler(Filters.document, head(photo_handler)))
    dp.add_handler(MessageHandler(Filters.audio, head(photo_handler)))
    dp.add_handler(MessageHandler(Filters.contact, head(organizer)))
    dp.add_handler(CallbackQueryHandler(call_back(callback)))
    dp.add_error_handler(error)
