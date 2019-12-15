from .Valid import *
from .MemberData import organizer, change_status
from .config import CHATS
from .Connect import send_connection, create_connection
from .Admin import send_pink, send_for_all


def message_handler(bot, update, member, *args):
    status = member.status
    if status < 15:
        organizer(bot, update, member)
        return
    elif member.status > 19:
        send_connection(bot, update, member)
        return
    elif update.message.text == "🏠خانه🏠":
        text = Message.objects.get(event="help")
        bot.sendMessage(member.tel, text.context, reply_markup=ReplyKeyboardMarkup(text.keyboard or []))
        member.status = 15
        member.save()
        return
    user = bot.getChatMember(CHATS, member.tel)
    if user.status == "left" or user.status == "kicked":
        not_valid_user(bot, update, member)
        return
    elif status == 15:
        change_status(bot, update, member)
        return
    elif status == 19:
        create_connection(member, update.message.text, bot)
        return
    elif status == 16:
        send_pink(bot, update, member)
        return
    elif status == 17:
        send_for_all(bot, update, member)
        return
    else:
        not_valid_data(bot, update, member)
        return


def photo_handler(bot, update, member):
    if member.status == 16:
        send_pink(bot, update, member)
    elif member.status == 17:
        send_for_all(bot, update, member)
    else:
        not_valid_data(bot, update, member)
        return
