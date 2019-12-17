from bot.models import Message, Member, Connection
from telegram import InlineKeyboardMarkup
from .convert import dict_to_button
from telegram import ReplyKeyboardMarkup
from .convert import text_to_keyboard
from .config import CHATS, Bot
from .SendAll import send_all


def create_connection(member1, member2username, bot, status=1):
    try:
        member2 = Member.objects.get(username=member2username)
        print(member2.name)
        Connection.objects.update_or_create(connect1=member1, connect2=member2, defaults={"status": status})
        message = Message.objects.get_or_create(event="connect_successful",
                                                defaults={"context": "connect_successful empty"})[0]
        member1.status = 20
        member1.save()
        if status == 1:
            member2.status = 21
            member2.save()
            bot.sendMessage(member2.tel, message.context,
                            reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard), resize_keyboard=True))
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
                        reply_markup=InlineKeyboardMarkup(dict_to_button(text_to_keyboard(message.keyboard)),
                                                          resize_keyboard=True))
        return
    link = '<a href="{}">{}</a>'.format("https://t.me/%s?start=%s" % (Bot, member.username),
                                        member.username + " _ " + member.last_name)
    text_add = "\n\n🎈کاربر:{}\n\n{}".format(link, CHATS)
    if update.message.text:
        update.message.text += text_add
    elif update.message.caption:
        if len(update.message.caption + text_add) > 1024:
            bot.sendMessage(member.tel, "تعداد کارکتر ارسالی شما باید کمتر از {} باشد".format(1024 - len(text_add)))
            return
        update.message.caption = (update.message.caption or "") + text_add
    if member.status == 20:
        connection = member.connector.filter(status__in=[1, 2]).first()
        a = ""
        if connection.status == 2:
            connection.status = 0
            member.status = 15
            member.save()
            connection.save()
        send_all(bot, update, users=[connection.connect2.tel])
    elif member.status == 21:
        connection = member.link.filter(status=1).first()
        send_all(bot, update, users=[connection.connect1.tel])
