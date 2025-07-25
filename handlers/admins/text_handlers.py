from telebot.types import Message, ReplyKeyboardRemove

from data.loader import bot, db
from keyboards.default import make_buttons
from config import ADMINS

admin_buttons_names = [
    "➕ Sayohatlar qo'shish",
    "➕ Mashhur joylar qo'shish",
    "➕ Ekskursiya jadvali qo'shish",
]

TRAVEL = {}

@bot.message_handler(func=lambda message: message.text == "👮‍♂️Admin buyruqlari")
def reaction_to_admin_commands(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "Admin buyruqlari",
                         reply_markup=make_buttons(admin_buttons_names, back=True))


@bot.message_handler(func=lambda message: message.text == "➕ Sayohatlar qo'shish")
def reaction_to_admin_commands(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Sayoxat nomini kiritng",
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_travel)


def get_name_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id] = {
        "name": message.text
    }
    msg = bot.send_message(chat_id, "Sayoxat narxini kiriting")
    bot.register_next_step_handler(msg, get_name_price)


def get_name_price(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["price"] = message.text
    msg = bot.send_message(chat_id, "Sayoxat davomiyligini(kun) kiriting")
    bot.register_next_step_handler(msg, get_name_days)


def get_name_days(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    days = int(message.text)
    name = TRAVEL[from_user_id]["name"]
    price = int(TRAVEL[from_user_id]["price"])
    db.insert_travel(name, price, days)
    bot.send_message(chat_id, "Sayoxat saqlandi!",
                     reply_markup=make_buttons(admin_buttons_names, back=True))