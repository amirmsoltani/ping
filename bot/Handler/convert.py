from telegram import InlineKeyboardButton
from json import loads


def dict_to_button(array):
    array2 = [[InlineKeyboardButton(**ob) for ob in l1] for l1 in array]
    return array2


def text_to_keyboard(text):
    if text is None:
        return []
    array = loads(text)
    return array
