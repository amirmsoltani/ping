from bot.models import Message, Category
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from math import ceil
from .convert import text_to_keyboard

valid_data = {0: "phone_not_valid", 1: "name_not_valid",
              2: "last_name_not_valid", 3: "gender_not_valid",
              4: "category",
              }
valid_status = {0: "request_phone", 1: "request_name", 2: "request_last_name",
                3: "request_gender", 4: "request_category",
                }


def category(bot, update, member):
    event = valid_status.get(member.status) or "status_not_set"
    message = Message.objects.get_or_create(event=event, defaults={"context": "%s empty" % event})[0]
    category = Category.objects.all()
    count = category.count()
    row = ceil(count / 12.0)
    rows = []
    for cat in category:
        button = InlineKeyboardButton(cat.name, callback_data="category&%s" % str(cat.id))
        if len(rows) == 0 or len(rows[-1]) == row:
            rows.append([button])
            continue
        rows[-1].append(button)
    rows.append([InlineKeyboardButton("تایید نهایی", callback_data="category&submit")])
    new_text = message.context + "\n\n دسته های انتخابی شما:\n"
    for cat in member.category.all():
        new_text += cat.name + "\n"
    bot.sendMessage(member.tel, new_text, reply_markup=InlineKeyboardMarkup(rows))


def not_valid_status(bot, update, member):
    status = member.status
    if status == 4:
        category(bot, update, member)
        return
    chat_id = update.message.chat_id
    event = valid_status.get(status) or "status_not_set"
    message = Message.objects.get_or_create(event=event, defaults={"context": "%s empty" % event})[0]
    keyboard = text_to_keyboard(message.keyboard)
    bot.sendMessage(chat_id, text=message.context,
                    reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))


def not_valid_data(bot, update, member):
    status = member.status
    chat_id = update.message.chat_id
    event = valid_data.get(status) or "request_not_valid"
    message = Message.objects.get_or_create(event=event, defaults={"context": "%s empty" % event})[0]
    bot.sendMessage(chat_id, text=message.context)


def not_valid_user(bot, update, member):
    message = Message.objects.get_or_create(event="user_add", defaults={"context": "user_add empty"})[0]
    bot.sendMessage(member.tel, message.context,
                    reply_markup=ReplyKeyboardMarkup(text_to_keyboard(message.keyboard), resize_keyboard=True))
