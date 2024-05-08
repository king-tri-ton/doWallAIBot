import sqlite3
from threading import Lock

# Создание блокировки для защиты от потоковых проблем
lock = Lock()

# Функция для получения соединения с базой данных
def get_connection():
    conn = sqlite3.connect('dowallaibot.db')
    return conn

def create_tables():
    conn = get_connection()
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

def add_user(tg_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (tg_id) VALUES (?)", (tg_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def add_image(tg_id, prompt, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (tg_id, prompt, image_url) VALUES (?, ?, ?)", (tg_id, prompt, image_url))
    conn.commit()
    conn.close()

def get_total_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    conn.close()
    return total_users
