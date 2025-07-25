from telebot.types import Message
from data.loader import bot, db
from config import TEXTS


@bot.message_handler(func=lambda message: message.text in TEXTS[db.get_lang(message.from_user.id)][101])
def reaction_to_packages(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Siz: {message.text} ni tangladingiz!!!")
    if message.text in ["⚙️Settings", "⚙️Настройки", "⚙️Sozlamalar"]:
        pass