from bot.models import Message
from .Valid import not_valid_status
from .Connect import create_connection
from telegram import ReplyKeyboardMarkup
from .convert import text_to_keyboard


def on_start(bot, update, member, *args):
    if member.status < 15:
        not_valid_status(bot, update, member)
        return
    elif (member.status == 19 or member.status == 15) and len(args) != 0 and create_connection(member, args[0], bot):
        return
    message = Message.objects.get_or_create(event="help", defaults={"context": "help empty"})[0]
    bot.sendMessage(update.message.chat_id, message.context,
                    reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard), resize_keyboard=True))


def on_help(bot, update, member, *args):
    if member.status < 15:
        not_valid_status(bot, update, member)
        return
    message = Message.objects.get_or_create(event="help", defaults={"context": "help empty"})[0]
    bot.sendMessage(update.message.chat_id, message.context)
