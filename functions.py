from config import IMAGE_FOLDER, AI_TOKEN
from openai import OpenAI
from db import db_manager
import requests
import time
import os

client = OpenAI(api_key=AI_TOKEN)

def generate_image_url(text, size, quality):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=text,
            size=size,
            quality=quality,
            n=1,
        )
        print(response.data[0].url)
        return response.data[0].url
        ## TESTING
        # return "https://via.placeholder.com/1024x1024"
    except Exception as e:
        # Error handling if an error occurred during image generation
        print(f"Error generating image: {str(e)}")
        return None


def download_image(image_url, save_path):
    # Attempting to load an image with retries on error
    retries = 3
    for _ in range(retries):
        try:
            with requests.get(image_url, stream=True, timeout=30) as r:
                if r.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(r.content)
                    return True
                else:
                    raise Exception("Failed to load image.")
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            time.sleep(1)  # Подождать перед повторной попыткой
    else:
        print("Failed to load image.")
        return False

def send_image(bot, message, text, image_path):
    # Sending an image to a user
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, reply_to_message_id=message.message_id)

    # Writing image data to a database
    db_manager.add_image(message.chat.id, text, image_path)

def download_and_send_image(bot, message, text, image_url):
    if image_url is None:
        bot.send_message(message.chat.id, "Failed to create image.")
        return

    # Downloading an image and saving it to the images folder
    image_path = os.path.join(IMAGE_FOLDER, f"{message.chat.id}_{message.message_id}.png")
    
    if download_image(image_url, image_path):
        send_image(bot, message, text, image_path)
