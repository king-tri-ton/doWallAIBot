
https://github.com/king-tri-ton/doWallAIBot/assets/53092931/c4a93538-438b-43fa-b991-93af583ffeb6

**Telegram Bot for Generating Images Based on Text Description Using OpenAI API**

---

This Telegram bot is designed to generate images based on textual descriptions using the image generation model from OpenAI. Users can send textual descriptions, and the bot uses the OpenAI API to generate images, which are then sent back to the user as an image file.

---

**Installation and Setup:**

1. **Install Dependencies:**

   Before using, make sure you have all the necessary dependencies installed. You can install them by running the following command:

   ```
   pip install -r requirements.txt
   ```

2. **Register Bot on Telegram:**

   - Register a new bot on Telegram following the instructions [here](https://core.telegram.org/bots#botfather).
   - Obtain the bot token from BotFather and save it.

3. **Get OpenAI API Key:**

   - Register on the [OpenAI website](https://openai.com/).
   - Obtain the API key by choosing the appropriate pricing plan.

4. **Configure Configuration File:**

   - Create a `config.py` file based on `exp.config.py`.
   - Fill in the fields `AI_TOKEN` (OpenAI API key), `BOT_TOKEN` (Telegram bot token), and `ADMIN_ID` (bot administrator's ID).

5. **Run the Bot:**

   - After configuring all necessary parameters, run the `bot.py` file:

   ```
   python bot.py
   ```

---

**Usage:**

1. **Command /start:**

   - Begin interacting with the bot by sending the command `/start`.
   - After executing this command, the bot will wait for you to send a textual description to generate an image.

2. **Sending Text Description:**

   - After sending the `/start` command, send the bot a textual description you want to convert into an image.
   - The bot will initiate the image generation process based on your description.

3. **Command /stats:**

   - To get usage statistics of the bot, send the command `/stats`.
   - This command is only available to the bot administrator.

4. **Receiving the Image:**

   - After generating the image, the bot will send you the result as an image file.

---

**Note:**

- Before usage, ensure all necessary libraries are installed, and you have correctly filled in the `config.py` file.
- Please note that using the OpenAI API may incur additional charges depending on your pricing plan.
- This bot is provided "as is" without any warranties or obligations. You use it at your own risk.

---

## Changelog

<details>
<summary><strong>Version 3.0.0</strong></summary>

- `bot.py`
    - Added handling for selecting image size and quality for text description.
    - Modified text message handler to consider the choice of image size and quality.
    - Added new functions: `process_text_description`, `generate_size_keyboard`, `process_size_selection`, `generate_quality_keyboard`, `process_quality_selection`.
    - Updated image generation handler to take into account the selected size and quality.
  
- `functions.py`
    - Changed signature of `generate_image_url` function to now accept additional parameters `size` and `quality`.
    - Updated `download_and_send_image` function to pass text description along with the image.
</details>


<details>
<summary><strong>Version 2.0.2</strong></summary>

- `bot.py`
    - Changed import of functions <strong>generate_image_url</strong> and <strong>download_and_send_image</strong> from the file <strong>functions.py</strong>.
    - Changed import of <strong>db</strong> to <strong>db_manager</strong> from the file <strong>db.py</strong>.
    - Instead of directly calling functions from the <strong>db</strong> module, now use the <strong>create_tables()</strong> method of <strong>db_manager</strong> instance.
    - Instead of directly calling the <strong>add_user</strong> function from the <strong>db</strong> module, now use the <strong>add_user()</strong> method of <strong>db_manager</strong> instance.
    - Instead of directly calling the <strong>get_total_users</strong> function from the <strong>db</strong> module, now use the <strong>get_total_users()</strong> method of <strong>db_manager</strong> instance.
    - The <strong>generate_image()</strong> function was changed to a method with the same name, now using functions from the <strong>functions.py</strong> file.
- `db.py`
    - Added a new class <strong>DatabaseManager</strong>.
    - Database operations are encapsulated within this class.
    - Initialized the <strong>DatabaseManager</strong> object with the default database name.
    - Use locking (<strong>Lock</strong>) to prevent threading issues when accessing the database simultaneously.
    - Database operations are performed within the lock context (<strong>with self.lock</strong>), ensuring safety during parallel access.
- `functions.py`
    - The <strong>generate_image_url()</strong> function now returns the URL of the generated image instead of sending it.
    - Added the <strong>download_image()</strong> function, which downloads the image from a URL and saves it to disk.
    - Added the <strong>send_image()</strong> function, which sends the image to the user and records image data in the database via the <strong>db_manager</strong> instance.
    - Added the <strong>download_and_send_image()</strong> function, which first downloads the image, then sends it to the user, and records image data in the database via the <strong>db_manager</strong> instance.
</details>

<details>
<summary><strong>Version 2.0.0</strong></summary>

- `exp.config.py`
    - <strong>Added</strong> variable `IMAGE_FOLDER` containing the path to the folder for saving images.
- `bot.py`
    - <strong>Added</strong> validation of the incoming text message length before processing to ensure the text is at least 10 characters long.
    - <strong>Added</strong> exception handling for errors that may occur during image generation using OpenAI. In case of an error, a message is sent to the user requesting to retry the request or contact the developer.
    - <strong>Changed</strong> the logic of image saving: now the image is downloaded and saved in the specified `images` folder with a name in the format `<tg_id>_<message_id>.png`.
    - <strong>Changed</strong> the method of sending the image to the user: now the image is sent as a file object rather than via URL.
- `db.py`
    - Added exception handling in the `add_user(tg_id)` function to prevent potential errors when adding a user to the database.
</details>

---

**License:**

This project is distributed under the [MIT License](https://choosealicense.com/licenses/mit/).

---

If you have any questions or suggestions for improving the project, feel free to contact me at mdolmatov99@gmail.com or via Telegram [@king_triton](https://t.me/king_triton). Thank you for using my bot!
