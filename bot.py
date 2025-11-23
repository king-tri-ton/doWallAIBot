from functions import generate_image_url, download_and_send_image
from config import BOT_TOKEN, ADMIN_ID
from db import db_manager
import telebot

# Create a bot instance using your token
bot = telebot.TeleBot(BOT_TOKEN)

# Creating tables in the database
db_manager.create_tables()

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Writing user data to the database
    db_manager.add_user(message.chat.id)
    bot.reply_to(message, "Hello! I can create an image from a text description.")

# /stats command handler
@bot.message_handler(commands=['stat'])
def show_stats(message):
    # Checking if a user is an administrator
    if message.from_user.id == ADMIN_ID:
        # Getting the number of users from the database
        total_users = db_manager.get_total_users()
        bot.reply_to(message, f"Number of users who used the bot: {total_users}")
    else:
        bot.reply_to(message, "You do not have permission to run this command.")

# Text message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if len(message.text) > 10:
        # Если текстовое описание длиннее 10 символов, считаем его описанием
        process_text_description(message)
    else:
        # Если текстовое описание короче 10 символов, запрашиваем размер
        bot.send_message(message.chat.id, "Choose image size:", reply_markup=generate_size_keyboard())
        bot.register_next_step_handler(message, process_size_selection)

# Function to process text description
def process_text_description(message):
    text = message.text  # Extracting text description
    # Asking the user to select image size
    bot.send_message(message.chat.id, "Choose image size:", reply_markup=generate_size_keyboard())
    # Storing text description to pass it to the next step
    bot.register_next_step_handler(message, process_size_selection, text)

# Function to generate keyboard for size selection
def generate_size_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("1024x1024", "1024x1792", "1792x1024")
    return keyboard

# Function to process size selection
def process_size_selection(message, text):
    size = message.text
    bot.send_message(message.chat.id, "Choose image quality:", reply_markup=generate_quality_keyboard())
    bot.register_next_step_handler(message, process_quality_selection, text, size)

# Function to generate keyboard for quality selection
def generate_quality_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("standard", "hd")
    return keyboard

# Function to process quality selection
def process_quality_selection(message, text, size):
    quality = message.text
    bot.send_message(message.chat.id, "I'm creating an image, please wait...", reply_markup=telebot.types.ReplyKeyboardRemove())
    # Generate images with text description, size and quality
    image_url = generate_image_url(text, size, quality)
    download_and_send_image(bot, message, text, image_url)
    bot.send_message(message.chat.id, "Image has been generated.")

# Running a bot
bot.infinity_polling(interval=0)