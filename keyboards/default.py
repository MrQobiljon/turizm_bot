from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import TEXTS


def phone_button(name):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(name, request_contact=True)
    markup.add(btn)
    return markup


def make_buttons(names: list, row_width: int = 2):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    buttons = []
    for name in names:
        btn = KeyboardButton(name)
        buttons.append(btn)
    markup.add(*buttons)
    return markup