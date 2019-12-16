from bot.models import Message, Member, Connection
from telegram import InlineKeyboardMarkup
from .convert import dict_to_button
from telegram import ReplyKeyboardMarkup
from .convert import text_to_keyboard


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
                            reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard)))
        bot.sendMessage(member1.tel, message.context,
                        reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard)))

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
    if member.status == 20:
        connection = member.connector.filter(status__in=[1, 2]).first()
        a = ""
        if connection.status == 2:
            connection.status = 0
            member.status = 15
            member.save()
            connection.save()
            a = "\n پاسخ ادمین"
            keyboard = text_to_keyboard(Message.objects.get(event="help").keyboard)
            bot.sendMessage(member.tel, "پاسخ ارسال شد", reply_markup=ReplyKeyboardMarkup(keyboard))
        bot.sendMessage(connection.connect2.tel, update.message.text + a)
    elif member.status == 21:
        connection = member.link.filter(status=1).first()
        bot.sendMessage(connection.connect1.tel, update.message.text)
