from bot.models import Message, Category
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .config import CHATS, Bot
from .Connect import create_connection


def release(bot, update, id):
    if update.message.text:
        bot.sendMessage(CHATS, update.message.text,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                            "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]))
    elif update.message.photo:
        bot.sendPhoto(CHATS, update.message.photo[0].file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    elif update.message.voice:
        bot.sendVoice(CHATS, update.message.voice.file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    elif update.message.video:
        bot.sendVideo(CHATS, update.message.video.file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    elif update.message.document:
        bot.sendDocument(CHATS, update.message.document.file_id, caption=update.message.caption or "",
                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                             "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                         ))
    elif update.message.audio:
        bot.sendAudio(CHATS, update.message.file.file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    bot.answerCallbackQuery(update.id, text="پست انتشار یافت", show_alert=True)


def callback(bot, update, member):
    data = update.data
    status = member.status
    if data == "yes_dc" and status in [20, 21]:
        connect = None
        member2 = None
        if status == 20:
            connect = member.connector.filter(status=1).first()
            member2 = connect.connect2
        elif status == 21:
            connect = member.link.filter(status=1).first()
            member2 = connect.connect1

        member.status = 15

        member.save()

        bot.deleteMessage(member.tel, update.message.message_id)
        message = Message.objects.get_or_create(event="dc_connect", defaults={"context": "dc_connect empty"})[0]
        bot.sendMessage(member.tel, message.context, reply_markup=ReplyKeyboardMarkup(message.keyboard or []))
        if connect.status == 1:
            bot.sendMessage(member2.tel, message.context, reply_markup=ReplyKeyboardMarkup(message.keyboard or []))
            member2.status = 15
            member2.save()
        connect.status = 0
        connect.save()
    elif data == "no_dc" and status in [20, 21]:
        bot.deleteMessage(member.tel, update.message.message_id)
    elif data == "delete":
        bot.deleteMessage(member.tel, update.message.message_id)
        return
    split_data = str.split(data, "&")
    if split_data[0] == "release":
        release(bot, update, split_data[1])
        return
    elif split_data[0] == "send answer":
        create_connection(member, split_data[1], bot, 2)
        return
    elif split_data[0] == "category":
        if split_data[1] == "submit":
            member.status = 15
            member.save()
            bot.deleteMessage(member.tel, update.message.message_id)
            m = Message.objects.get_or_create(event="register", defaults={"context": "register empty"})[0]
            bot.sendMessage(member.tel, m.context, reply_markup=ReplyKeyboardMarkup(m.keyboard or []))
            return
        category = Category.objects.get(id=int(split_data[1]))
        if member.category.filter(id=int(split_data[1])).count() > 0:
            member.category.remove(category)
            bot.answerCallbackQuery(update.id, text="موضوع %s از دسته بندی شما حذف شد" % category.name,
                                    show_alert=True)
        else:
            member.category.add(category)
            bot.answerCallbackQuery(update.id, text="موضوع %s به دسته بندی های شما اضافه شد" % category.name,
                                    show_alert=True)
        member.save()
        text = update.message.text
        split_text = text.split("\n\n دسته های انتخابی شما:")
        new_text = split_text[0] + "\n\n دسته های انتخابی شما:\n"
        for cat in member.category.all():
            new_text += cat.name + "\n"
        bot.editMessageText(chat_id=member.tel, message_id=update.message.message_id,
                            reply_markup=update.message.reply_markup, text=new_text)
        return
    elif split_data[0] == "sendto":
        member.status = 17
        member.send = split_data[1]
        member.save()
        message = Message.objects.get_or_create(event="sendto", defaults={"context": "sendto request empty"})[0]
        bot.sendMessage(member.tel, text=message.context, reply_markup=ReplyKeyboardMarkup(message.keyboard or []))
        return
