from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from data.loader import bot, db
from config import TEXTS
from keyboards.default import phone_button

REGISTER = {}


@bot.callback_query_handler(func=lambda call: call.data in ["uz", "ru", "en"])
def reaction_to_lang(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = call.data
    db.update_lang(lang, from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    text = TEXTS[lang][1]
    msg = bot.send_message(chat_id, text)
    bot.register_next_step_handler(msg, get_name)


def get_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    text = TEXTS[lang][1]
    if message.text:
        REGISTER[from_user_id] = {
            "full_name": message.text
        }
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)
    else:
        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)


def get_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    if message.contact:
        phone_number = message.contact.phone_number
        full_name = REGISTER[from_user_id]["full_name"]
        db.save_phone_number_and_full_name(full_name, phone_number, from_user_id)
        bot.send_message(chat_id, TEXTS[lang][3], reply_markup=ReplyKeyboardRemove())
    else:
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)