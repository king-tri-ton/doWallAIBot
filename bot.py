import telebot
from openai import OpenAI
from config import *
import requests
import db
import os

# Создание экземпляра бота с использованием вашего токена
bot = telebot.TeleBot(BOT_TOKEN)

# Инициализация клиента OpenAI
client = OpenAI(api_key=AI_TOKEN)

# Создание таблиц в базе данных
db.create_tables()

# Создание папки, если ее нет
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Запись данных пользователя в базу данных
    db.add_user(message.chat.id)
    bot.reply_to(message, "Привет! Я могу создать обои по текстовому описанию для твоего телефона.")

# Обработчик команды /stats
@bot.message_handler(commands=['stats'])
def show_stats(message):
    # Проверка, является ли пользователь администратором
    if message.from_user.id == ADMIN_ID:
        # Получение количества пользователей из базы данных
        total_users = db.get_total_users()
        bot.reply_to(message, f"Количество пользователей, воспользовавшихся ботом: {total_users}")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def generate_image(message):
    # Проверка длины сообщения
    if len(message.text) < 10:
        bot.send_message(message.chat.id, "Введите текст длиной не менее 10 символов.")
        return

    # Отправка оповещения о начале процесса генерации
    bot.send_message(message.chat.id, "Создаю обои, пожалуйста ожидайте...")

    # Генерация изображения с использованием OpenAI
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=message.text,
            size="1024x1792",
            quality="standard",
            n=1,
        )

        # Получение URL сгенерированного изображения
        image_url = response.data[0].url
        # print(image_url)

        # Скачивание изображения и сохранение в папку images
        image_path = os.path.join(IMAGE_FOLDER, f"{message.chat.id}_{message.message_id}.png")
        with requests.get(image_url, stream=True) as r:
            if r.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(r.content)
            else:
                bot.send_message(message.chat.id, "Не удалось загрузить изображение.")

        # Запись данных об изображении в базу данных
        db.add_image(message.chat.id, message.text, image_path)

        # Отправка изображения пользователю
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)
    except Exception as e:
        # bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, f"Произошла ошибка, прошу прощения за предоcтавленные неудобства, попробуйте еще раз или свяжитесь с разработчиком @king_triton")

# Запуск бота
bot.infinity_polling(interval=0)