from data.loader import bot, db
import handlers


if __name__ == '__main__':
    bot.remove_webhook()
    db.create_table_users()
    # db.drop_table_travels()
    db.create_table_travels()
    db.create_table_images()
    bot.infinity_polling()