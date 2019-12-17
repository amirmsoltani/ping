from bot.models import Member, Message, Category
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from math import ceil
from .SendAll import send_all
from .convert import text_to_keyboard
from .config import Bot, CHATS


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
    link = '<a href="{}">{}</a>'.format("https://t.me/%s?start=%s" % (Bot, member.username),
                                        member.username + " _ " + member.last_name)
    text_add = "\n\n🎈کاربر:{}\n\n{}".format(link, CHATS)
    text = ""
    if update.message.text:
        text = update.message.text + text_add
    elif update.message.caption:
        if len(update.message.caption + text_add) > 1024:
            bot.sendMessage(member.tel, "تعداد کارکتر ارسالی شما باید کمتر از {} باشد".format(1024 - len(text_add)))
            return
        text = (update.message.caption or "") + text_add
    message = Message.objects.get_or_create(event="send_pink_suc", defaults={"context": "send_pink_suc empty"})[0]
    bot.sendMessage(member.tel, message.context, reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard),resize_keyboard=True))
    member.status = 15
    member.save()
    if update.message.text:
        bot.sendMessage(admin.tel, text,
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode="HTML")
    elif update.message.photo:
        bot.sendPhoto(admin.tel, caption=text,
                      reply_markup=InlineKeyboardMarkup(keyboard), photo=update.message.photo[0].file_id,
                      parse_mode="HTML")
    elif update.message.voice:
        bot.sendVoice(admin.tel, caption=text,
                      reply_markup=InlineKeyboardMarkup(keyboard), voice=update.message.voice.file_id,
                      parse_mode="HTML")
    elif update.message.video:
        bot.sendVideo(admin.tel, caption=text,
                      reply_markup=InlineKeyboardMarkup(keyboard), video=update.message.video.file_id,
                      parse_mode="HTML")
    elif update.message.document:
        bot.sendDocument(admin.tel, caption=text,
                         reply_markup=InlineKeyboardMarkup(keyboard), document=update.message.document.file_id,
                         parse_mode="HTML")
    elif update.message.audio:
        bot.sendAudio(admin.tel, caption=text,
                      reply_markup=InlineKeyboardMarkup(keyboard), audio=update.message.audio.file_id,
                      parse_mode="HTML")


def send_panel(bot, member):
    rows = [[InlineKeyboardButton(text="دریافت شماره های دیتابیس", callback_data="give&numbers")],
            [InlineKeyboardButton(text="ارسال پیام به همه پسران", callback_data="sendto&boys"),
             InlineKeyboardButton(text="ارسال پیام به همه دختران", callback_data="sendto&girls")]]
    categorys = Category.objects.all()
    count = categorys.count()
    row = ceil(count / 12.0)
    for cat in categorys:
        button = InlineKeyboardButton("ارسال پیام به " + cat.name, callback_data="sendto&%s" % str(cat.id))
        if len(rows[-1]) >= row:
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
    send_all(bot, update, users)
    message = \
        Message.objects.get_or_create(event="message_admin_send", defaults={"context": "message_admin_send empty"})[
            0]
    bot.sendMessage(member.tel, message.context, reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard),resize_keyboard=True))


def get_number(bot, update, member):
    members = Member.objects.all().values("name", "last_name", "phone")
    with open("/home2/wirgoola/ping/public/number.txt", 'w') as f:
        for m in members:
            f.write("{} , {} , {} \n".format(m['name'], m['last_name'], m['phone']))
    bot.sendDocument(member.tel, caption="لینک دانلود:%s" % "https://wirgoolads.ir/static/number.txt",
                     document=open("/home2/wirgoola/ping/public/number.txt", 'rb'))
    return
