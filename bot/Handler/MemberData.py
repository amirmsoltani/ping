from bot.models import Member, Message
from .Valid import not_valid_data, not_valid_status
import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
from .convert import dict_to_button
from .Admin import send_panel
from .convert import text_to_keyboard

logger = logging.getLogger(__name__)


def organizer(bot, update, member, *args):
    chat_id = update.message.chat_id
    if member is None:
        member = Member.objects.get(tel=chat_id)
    if member.status == 0 and update.message.contact is not None:
        if update.message.contact.user_id == chat_id:
            member.phone = update.message.contact.phone_number
            member.status = 1
            member.save()
            not_valid_status(bot, update, member)
        else:
            not_valid_data(bot, update, member)
    elif member.status == 0:
        if len(update.message.text) == 11:
            member.status = 1
            member.phone = update.message.text
            member.save()
            not_valid_status(bot, update, member)
        else:
            not_valid_data(bot, update, member)
    elif member.status == 1:
        if len(update.message.text) < 100:
            member.name = update.message.text
            member.status = 2
            member.save()
            not_valid_status(bot, update, member)
        else:
            not_valid_data(bot, update, member)
    elif member.status == 2:
        if len(update.message.text) < 100:
            member.last_name = update.message.text
            member.status = 3
            member.save()
            not_valid_status(bot, update, member)
        else:
            not_valid_data(bot, update, member)
    elif member.status == 3:
        text = update.message.text
        if text == "پسرم":
            member.gender = 1
            member.status = 4
            member.save()
            not_valid_status(bot, update, member)
        elif text == "دخترم":
            member.gender = 0
            member.status = 4
            member.save()
            not_valid_status(bot, update, member)
        else:
            not_valid_data(bot, update, member)
    elif member.status == 4:
        not_valid_data(bot, update, member)
        return
    else:
        not_valid_data(bot, update, member)


def change_status(bot, update, member):
    message = update.message.text

    if message == "راهنما⛔️":
        text = Message.objects.get(event="help")
        bot.sendMessage(member.tel, text.context, reply_markup=ReplyKeyboardMarkup(text_to_keyboard(text.keyboard)))
        return
    elif message == "👨‍❤️‍💋‍👨ارسال پینک🏖":
        text = Message.objects.get_or_create(event="send_pink", defaults={"context": "send_pink empty"})[0]
        bot.sendMessage(member.tel, text.context, reply_markup=ReplyKeyboardMarkup(text_to_keyboard(text.keyboard)))
        member.status = 16
        member.save()
        return
    elif message == "👙اتصال به پینکر💒":
        text = Message.objects.get_or_create(event="connect_to_pink", defaults={"context": "connect_to_pink empty"})[0]
        bot.sendMessage(member.tel, text.context, reply_markup=ReplyKeyboardMarkup(text_to_keyboard(text.keyboard)))
        member.status = 19
        member.save()
        return
    elif message == "پنل مدیریت":
        text = Message.objects.get_or_create("admin_panel", defaults={"context": "admin_panel empty"})[0]
        bot.sendMessage(member.tel, text.context,
                        reply_markup=InlineKeyboardMarkup(dict_to_button(text_to_keyboard(text.keyboard))))
        return
    elif update.message.text == "پنل" and member.type == 5:
        send_panel(bot, member)
        return
    else:
        not_valid_data(bot, update, member)
        return
