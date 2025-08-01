import sqlite3


class Database:
    def __init__(self, db_name: str = "main.db"):
        self.database = db_name

    def execute(self, sql, *args, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        with sqlite3.connect(self.database) as db:
            cursor = db.cursor()
            cursor.execute(sql, args)

            res = None

            if fetchone:
                res = cursor.fetchone()
            elif fetchall:
                res = cursor.fetchall()

            if commit:
                db.commit()
        return res

    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id INTEGER NOT NULL UNIQUE,
            full_name TEXT,
            phone_number VARCHAR(13),
            lang VARCHAR(3)
        )'''
        self.execute(sql, commit=True)

    def insert_telegram_id(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES (?)'''
        self.execute(sql, telegram_id, commit=True)

    def update_lang(self, lang, telegram_id):
        sql = '''UPDATE users SET lang = ? WHERE telegram_id = ?'''
        self.execute(sql, lang, telegram_id, commit=True)

    def get_user(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = ?'''
        return self.execute(sql, telegram_id, fetchone=True)

    def get_lang(self, telegram_id):
        sql = '''SELECT lang FROM users WHERE telegram_id = ?'''
        return self.execute(sql, telegram_id, fetchone=True)[0]

    def save_phone_number_and_full_name(self, full_name, phone_number, telegram_id):
        sql = '''UPDATE users SET full_name = ?, phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, full_name, phone_number, telegram_id, commit=True)

    def create_table_travels(self):
        sql = '''CREATE TABLE IF NOT EXISTS travels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_uz TEXT,
            name_en TEXT,
            name_ru TEXT,
            price INTEGER,
            days INTEGER
        )'''
        self.execute(sql, commit=True)

    def drop_table_travels(self):
        sql = '''DROP TABLE IF EXISTS travels'''
        self.execute(sql, commit=True)

    def insert_travel(self, name_uz, name_en, name_ru, price, days):
        sql = '''INSERT INTO travels(name_uz, name_en, name_ru, price, days) VALUES (?, ?, ?, ?, ?)
        RETURNING id'''
        return self.execute(sql, name_uz, name_en, name_ru, price, days, commit=True, fetchone=True)[0]

    def select_travels(self, lang):
        sql = f'''SELECT id, name_{lang} FROM travels'''
        return self.execute(sql, fetchall=True)

    def select_travels_with_images(self, travel_id, lang):
        sql = f'''SELECT travels.id, travels.name_{lang}, images.id, images.image FROM travels JOIN images ON images.travel_id = travels.id WHERE travels.id = ?'''
        return self.execute(sql, travel_id, fetchall=True)

    def create_table_images(self):
        sql = '''CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            travel_id INTEGER REFERENCES travels(id)
        )'''
        self.execute(sql, commit=True)

    def insert_image(self, image: str, travel_id: int):
        sql = '''INSERT INTO images(image, travel_id) VALUES (?, ?)'''
        self.execute(sql, image, travel_id, commit=True)