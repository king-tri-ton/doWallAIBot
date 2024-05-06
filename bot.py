import telebot
from openai import OpenAI
from config import AI_TOKEN, BOT_TOKEN, ADMIN_ID
import requests
import db

# Создание экземпляра бота с использованием вашего токена
bot = telebot.TeleBot(BOT_TOKEN)

# Инициализация клиента OpenAI
client = OpenAI(api_key=AI_TOKEN)

# Создание таблиц в базе данных
db.create_tables()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Запись данных пользователя в базу данных
    db.add_user(message.chat.id)
    bot.reply_to(message, "Привет! Я могу создать обои для твоего телефона. Просто отправь мне текст.")

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
    # Отправка оповещения о начале процесса генерации
    bot.send_message(message.chat.id, "Создаю обои, пожалуйста ожидайте...")

    # Генерация изображения с использованием OpenAI
    response = client.images.generate(
        model="dall-e-3",
        prompt=message.text,
        size="1024x1792",
        quality="standard",
        n=1,
    )

    # Получение URL сгенерированного изображения
    image_url = response.data[0].url
    print(image_url)

    # Запись данных об изображении в базу данных
    db.add_image(message.chat.id, message.text, image_url)

    # Получение содержимого изображения из URL
    with requests.get(image_url, stream=True) as r:
        # Проверка статуса запроса
        if r.status_code == 200:
            # Отправка изображения пользователю по частям
            bot.send_photo(message.chat.id, photo=r.raw, reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "Не удалось загрузить изображение.")

# Запуск бота
bot.polling()