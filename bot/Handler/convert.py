from telegram import InlineKeyboardButton


def dict_to_button(array):
    array2 = [[InlineKeyboardButton(**ob) for ob in l1] for l1 in array]
    return array2
