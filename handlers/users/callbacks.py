from telebot.types import CallbackQuery
from data.loader import bot


@bot.callback_query_handler(func=lambda call: call.data in ["uz", "ru", "en"])
def reaction_to_lang(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
