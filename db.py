import sqlite3
from threading import Lock

class DatabaseManager:
    def __init__(self, db_name='dowallaibot.db'):
        self.db_name = db_name
        self.lock = Lock()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                tg_id INTEGER UNIQUE
                            )''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                                id INTEGER PRIMARY KEY,
                                tg_id INTEGER,
                                prompt TEXT,
                                image_url TEXT
                            )''')
            conn.commit()
            conn.close()

    def add_user(self, tg_id):
        with self.lock:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (tg_id) VALUES (?)", (tg_id,))
                conn.commit()
                conn.close()
            except Exception as e:
                print(e)

    def add_image(self, tg_id, prompt, image_url):
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO images (tg_id, prompt, image_url) VALUES (?, ?, ?)", (tg_id, prompt, image_url))
            conn.commit()
            conn.close()

    def get_total_users(self):
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            conn.close()
            return total_users

# Создание экземпляра менеджера базы данных
db_manager = DatabaseManager()
