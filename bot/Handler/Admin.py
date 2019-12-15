from bot.models import Member, Message, Category
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from math import ceil
from .SendAll import send_all


def send_pink(bot, update, member):
    admin = Member.objects.filter(type=5).first()
    keyboard = [
        [
            InlineKeyboardButton("انشار", callback_data="release&%s" % member.username),
            InlineKeyboardButton("خذف", callback_data="delete")
        ],
        [
            InlineKeyboardButton("ارسال پاسخ", callback_data="send answer&%s" % str(member.username)),
            InlineKeyboardButton("کاربر",
                                 callback_data="user&%s" % str(update.message.from_user.username or member.phone))
        ]
    ]
    message = Message.objects.get_or_create(event="send_pink_suc", defaults={"context": "send_pink_suc empty"})[0]
    bot.sendMessage(member.tel, message.context, reply_markup=ReplyKeyboardMarkup(message.keyboard or []))
    member.status = 15
    member.save()
    if update.message.text:
        bot.sendMessage(admin.tel, update.message.text,
                        reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.message.photo:
        bot.sendPhoto(admin.tel, caption=(update.message.caption or ""),
                      reply_markup=InlineKeyboardMarkup(keyboard), photo=update.message.photo[0].file_id)
    elif update.message.voice:
        bot.sendVoice(admin.tel, caption=(update.message.caption or ""),
                      reply_markup=InlineKeyboardMarkup(keyboard), voice=update.message.voice.file_id)
    elif update.message.video:
        bot.sendVideo(admin.tel, caption=(update.message.caption or ""),
                      reply_markup=InlineKeyboardMarkup(keyboard), video=update.message.video.file_id)
    elif update.message.document:
        bot.sendDocument(admin.tel, caption=(update.message.caption or ""),
                         reply_markup=InlineKeyboardMarkup(keyboard), document=update.message.document.file_id)
    elif update.message.audio:
        bot.sendAudio(admin.tel, caption=(update.message.caption or ""),
                      reply_markup=InlineKeyboardMarkup(keyboard), audio=update.message.audio.file_id)


def send_panel(bot, member):
    rows = [[InlineKeyboardButton(text="دریافت شماره های دیتابیس", callback_data="give&numbers")],
            [InlineKeyboardButton(text="ارسال پیام به همه پسران", callback_data="sendto&boys"),
             InlineKeyboardButton(text="ارسال پیام به همه دختران", callback_data="sendto&girls")]]
    categorys = Category.objects.all()
    count = categorys.count()
    row = ceil(count / 12.0)
    for cat in categorys:
        button = InlineKeyboardButton("ارسال پیام به " + cat.name, callback_data="sendto&%s" % str(cat.id))
        if len(rows) == 0 or len(rows[-1]) == row:
            rows.append([button])
            continue
        rows[-1].append(button)
    message = Message.objects.get_or_create(event="panel", defaults={"context": "panel request empty"})[0]
    bot.sendMessage(member.tel, message.context, reply_markup=InlineKeyboardMarkup(rows))


def send_for_all(bot, update, member):
    member.status = 15
    member.save()
    users = []
    if member.send == "boys":
        users = Member.objects.values("tel").filter(gender=1)
    elif member.send == "girls":
        users = Member.objects.values("tel").filter(gender=0)
    else:
        cat = Category.objects.get(id=int(member.send))
        users = cat.member_set.values("tel").all()
    users = [user['tel'] for user in users]
    send_all(bot, update, member, users)
    message = \
        Message.objects.get_or_create(event="message_admin_send", defaults={"context": "message_admin_send empty"})[
            0]
    bot.sendMessage(member.tel, message.context, reply_markup=ReplyKeyboardMarkup(message.keyboard or []))
