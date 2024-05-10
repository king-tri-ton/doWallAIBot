from config import IMAGE_FOLDER, AI_TOKEN
from openai import OpenAI
from db import db_manager
import requests
import time
import os

# Инициализация клиента OpenAI
client = OpenAI(api_key=AI_TOKEN)

def generate_image_url(text):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=text,
            size="1024x1024", # 1024x1024, 1024x1792, 1792x1024
            quality="standard", # standard, hd
            n=1,
        )
        print(response.data[0].url)
        return response.data[0].url
    except Exception as e:
        # Обработка ошибок, если произошла ошибка при генерации изображения
        print(f"Error generating image: {str(e)}")
        return None

def download_image(image_url, save_path):
    # Попытка загрузки изображения с повторными попытками при ошибке
    retries = 3
    for _ in range(retries):
        try:
            with requests.get(image_url, stream=True, timeout=30) as r:
                if r.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(r.content)
                    return True
                else:
                    raise Exception("Не удалось загрузить изображение.")
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {str(e)}")
            time.sleep(1)  # Подождать перед повторной попыткой
    else:
        print("Не удалось загрузить изображение.")
        return False

def send_image(bot, message, image_path):
    # Отправка изображения пользователю
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)

    # Запись данных об изображении в базу данных
    db_manager.add_image(message.chat.id, message.text, image_path)

def download_and_send_image(bot, message, image_url):
    if image_url is None:
        bot.send_message(message.chat.id, "Не удалось создать изображение.")
        return

    # Скачивание изображения и сохранение в папку images
    image_path = os.path.join(IMAGE_FOLDER, f"{message.chat.id}_{message.message_id}.png")
    
    if download_image(image_url, image_path):
        send_image(bot, message, image_path)
