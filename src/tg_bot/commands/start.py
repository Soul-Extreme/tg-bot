"""
File        : start.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /start command for the SE Telegram Bot
"""

import os

import telebot
import requests

from src.resources.dynamodb_table import DynamoDBTable
from src.resources.table_names import Tables, TABLE_KEYS


# ======================================================================================================================


def command_start(bot: telebot.TeleBot, message):
    """
    Runs through the /start command flow:

    1. Checks for user in DynamoDB Personal Particulars Table
    2a. If user doesn't exist; Prompt Registration through inline keyboard
    2b. If user exists; greet

    :param bot: The telebot invoking this command.
    :param message: The message received from the telegram server
    """

    personal_particulars_table = DynamoDBTable(
        Tables.PERSONAL_PARTICULARS.value, TABLE_KEYS[Tables.PERSONAL_PARTICULARS]
    )

    chat_id = message.chat.id
    user = personal_particulars_table.get_item(chat_id)

    if not user:
        # If user cannot be found, we prompt registration
        registration_prompt_message = (
            f"Welcome to the Soul Extreme Telegram Bot!\nYour <b>user ID</b> is\n<code>{chat_id}</code>\nCopy and "
            f"paste this into the user ID field on the registration form as shown in the attached image.\n\nPlease"
            f"click on the button to register for Soul Extreme.\n\nYou should receive a confirmation message once "
            f"you've registered. If you do not, please contact a committee member."
        )

        bot.send_message(
            chat_id,
            text=registration_prompt_message,
            reply_markup=gen_registration_keyboard_markup(chat_id),
        )
    else:
        name = user["preferred_name"] if user["preferred_name"] else user["full_name"]
        bot.send_message(chat_id, f"Welcome back {name}! How may I assist you?")


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


def gen_registration_keyboard_markup(chat_id):
    """
    Creates the inline keyboard to prompt Registration

    :param chat_id: The chat_id that will be POSTed to the Google form for registration
    :return: The markup for the inline keyboard
    """

    # The values in each button for an inline keyboard will only execute the first kwarg. Multiple are not supported!
    markup = telebot.util.quick_markup(
        {"Register": {"url": "https://forms.gle/LwbPKfyENvbnCkN28"}},
        row_width=1,
    )

    return markup
