from bot.models import Message, Category
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .config import CHATS, Bot,rel
from .Connect import create_connection
from .convert import text_to_keyboard
from .Admin import get_number
from math import ceil
from .SendAll import send_all


def release(bot, update, id):
    if update.message.text:
        bot.sendMessage(CHATS(), update.message.text,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                            "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]))
    elif update.message.photo:
        bot.sendPhoto(CHATS(), update.message.photo[0].file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    elif update.message.voice:
        bot.sendVoice(CHATS(), update.message.voice.file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    elif update.message.video:
        bot.sendVideo(CHATS(), update.message.video.file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    elif update.message.document:
        bot.sendDocument(CHATS(), update.message.document.file_id, caption=update.message.caption or "",
                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                             "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                         ))
    elif update.message.audio:
        bot.sendAudio(CHATS(), update.message.file.file_id, caption=update.message.caption or "",
                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                          "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, id))]]
                      ))
    bot.answerCallbackQuery(update.id, text="پست انتشار یافت", show_alert=True)


def get_cat(user_cat):
    category = Category.objects.all()
    count = category.count()
    row = ceil(count / 12.0)
    rows = []
    s = ""
    for cat in category:
        s = ""
        if cat in user_cat:
            s = "✅"
        button = InlineKeyboardButton(cat.name + s, callback_data="category&%s" % str(cat.id))
        if len(rows) == 0 or len(rows[-1]) == row:
            rows.append([button])
            continue
        rows[-1].append(button)
    rows.append([InlineKeyboardButton("تایید نهایی", callback_data="category&submit")])
    return rows


def callback(bot, update, member):
    data = update.data
    status = member.status
    if data == "yes_dc" and status in [20, 21]:
        member.connect = None
        member.answer = 0

        member.status = 15

        member.save()

        bot.deleteMessage(member.tel, update.message.message_id)
        message = Message.objects.get_or_create(event="dc_connect", defaults={"context": "dc_connect empty"})[0]
        bot.sendMessage(member.tel, message.context,
                        reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard), resize_keyboard=True))
    elif data == "no_dc" and status in [20, 21]:
        bot.deleteMessage(member.tel, update.message.message_id)
    elif data == "delete":
        bot.deleteMessage(member.tel, update.message.message_id)
        return
    split_data = str.split(data, "&")
    if split_data[0] == "release":
        send_all(bot, update, [rel()], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            "اتصال به پینکر", url="https://t.me/%s?start=%s" % (Bot, split_data[1]))]]))
        bot.answerCallbackQuery(update.id, text="پست انتشار یافت", show_alert=True)
        return
    elif split_data[0] == "send answer":
        create_connection(member, split_data[1], bot, split_data[2])
        return
    elif split_data[0] == "category":
        if split_data[1] == "submit":
            member.status = 15
            member.save()
            bot.deleteMessage(member.tel, update.message.message_id)
            m = Message.objects.get_or_create(event="register", defaults={"context": "register empty"})[0]
            bot.sendMessage(member.tel, m.context,
                            reply_markup=ReplyKeyboardMarkup(text_to_keyboard(m.keyboard), resize_keyboard=True))
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
        user_cat = member.category.all()
        for cat in user_cat:
            new_text += cat.name + "\n"

        bot.editMessageText(chat_id=member.tel, message_id=update.message.message_id,
                            reply_markup=InlineKeyboardMarkup(get_cat(user_cat)), text=new_text)
        return
    elif split_data[0] == "sendto":
        member.status = 17
        member.send = split_data[1]
        member.save()
        message = Message.objects.get_or_create(event="sendto", defaults={"context": "sendto request empty"})[0]
        bot.sendMessage(member.tel, text=message.context,
                        reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard), resize_keyboard=True))
        return
    elif split_data[0] == "user" and member.type == 5:
        bot.answerCallbackQuery(update.id, text=split_data[1], show_alert=True)
        bot.sendMessage(member.tel, split_data[1])
        return
    elif split_data[0] == "give" and member.type == 5:
        get_number(bot, update, member)
        return
