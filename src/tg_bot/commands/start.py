"""
File        : start.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /start command for the SE Telegram Bot
"""

import telebot
import requests

from src.resources.telegram_bot_instance import SE_TELEGRAM_BOT
from src.resources.dynamodb_table import DynamoDBTable
from src.resources.table_names import Tables, TABLE_KEYS


# ======================================================================================================================

@SE_TELEGRAM_BOT.message_handler(commands=['start'])
def command_start(bot: telebot.TeleBot, message):
    """
    Runs through the /start command flow:

    1. Checks for user in DynamoDB Personal Particulars Table
    2a. If user doesn't exist; Prompt Registration through inline keyboard
    2b. If user exists; greet

    :param bot: The telegram bot handling this message
    :param message: The message received from the telegram server
    """

    personal_particulars_table = DynamoDBTable(
        Tables.PERSONAL_PARTICULARS.value,
        TABLE_KEYS[Tables.PERSONAL_PARTICULARS]
    )

    user_id = message.chat.id
    user_item = personal_particulars_table.get_item(user_id)

    if not user_item:
        # If user cannot be found, we prompt registration
        registration_prompt_message = f"""
            Welcome to the Soul Extreme Telegram Bot!\n\n
            You are currently not registered as a member. Please click on the button to register for Soul Extreme.
        """

        bot.send_message(
            user_id,
            text=registration_prompt_message,
            reply_markup=gen_registration_keyboard_markup(user_id)
        )
    else:
        bot.send_message(user_id, f"Welcome back {user_id}!")


# ======================================================================================================================
# HELPERS
# ======================================================================================================================

def gen_registration_keyboard_markup(chat_id):
    """
    Creates the inline keyboard to prompt Registration

    :param chat_id: The chat_id that will be POSTed to the Google form for registration
    :return: The markup for the inline keyboard
    """
    markup = telebot.util.quick_markup({
        'Register': {
            'url': "https://forms.gle/LwbPKfyENvbnCkN28"
            # 'callback_data': f"registration{chat_id}"
        }
    }, row_width=1)

    return markup


# @SE_TELEGRAM_BOT.callback_query_handlers(func=lambda call: call.data.startswith("registration"))
# def handle_registration(call):
#     """
#     POST chat_id to google form. The chat_id field on the form is hidden from the user.
#     """
#     form_url = "https://forms.gle/LwbPKfyENvbnCkN28"
#     chat_id = call.data.removeprefix("registration")
#
#     response = requests.post(form_url, json={
#         "chat_id": chat_id
#     })
#
#     if response.status_code != 200:
#         print("Error sending data to Google Form")
