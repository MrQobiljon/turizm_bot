from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def lang_buttons():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🇺🇿O'zbek", callback_data="uz")
    btn2 = InlineKeyboardButton("🇬🇧English", callback_data="en")
    btn3 = InlineKeyboardButton("🇷🇺Русский", callback_data="ru")
    markup.add(btn1, btn2, btn3)
    return markup


def travels_buttons(travels_list):
    markup = InlineKeyboardMarkup(row_width=2)
    for travel in travels_list:
        travel_id, travel_name = travel
        btn = InlineKeyboardButton(travel_name, callback_data=f"travel_{travel_id}")
        markup.add(btn)
    return markup