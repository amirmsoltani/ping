from bot.models import Message, Member
from .convert import dict_to_button
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .convert import text_to_keyboard
from .config import CHATS, Bot
from .SendAll import send_all


def create_connection(member1, member2username, bot, answer=None):
    try:
        member2 = Member.objects.get(username=member2username)
        member1.connect = member2
        message = Message.objects.get_or_create(event="connect_successful",
                                                defaults={"context": "connect_successful empty"})[0]
        member1.status = 20
        if answer is not None:
            member1.answer = int(answer)
        member1.save()
        bot.sendMessage(member1.tel, message.context,
                        reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard), resize_keyboard=True))

        return True
    except Member.DoesNotExist:
        message = \
            Message.objects.get_or_create(event="user_not_exist", defaults={"context": "user_not_exist empty"})[0]
        bot.sendMessage(member1.tel, message.context)
        return False


def send_connection(bot, update, member):
    if update.message.text == "❌قطع اتصال❌":
        message = Message.objects.get_or_create(event="disconnect", defaults={"context": "disconnect empty"})[0]
        bot.sendMessage(member.tel, message.context,
                        reply_markup=InlineKeyboardMarkup(dict_to_button(text_to_keyboard(message.keyboard))))
        return
    link = '<a href="{}">{}</a>'.format("https://t.me/%s?start=%s" % (Bot, member.username),
                                        member.username + "\n🎈| " + member.last_name) + " |"
    text_add = "\n\n🎈پینکرکد:{}\n\n{}".format(link, CHATS())
    if update.message.text:
        update.message.text += text_add
    else:
        if len((update.message.caption or "") + text_add) > 1024:
            bot.sendMessage(member.tel, "تعداد کارکتر ارسالی شما باید کمتر از {} باشد".format(1024 - len(text_add)))
            return
        update.message.caption = (update.message.caption or "") + text_add

    keyboard = text_to_keyboard(Message.objects.get(event="help").keyboard)
    bot.sendMessage(member.tel, "پیام ارسال شد",
                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    send_all(bot, update, users=[member.connect.tel], reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("ارسال پاسخ",
                             callback_data="send answer&{}&{}".format(member.username, update.message.message_id))]]),
             reply_to_message_id=int(member.answer)or None)
    member.status = 15
    member.answer = 0
    member.connect = None
    member.save()
