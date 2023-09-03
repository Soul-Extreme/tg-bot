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


def command(bot: telebot.TeleBot, message):
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
        registration_prompt_message = f""" Welcome to the Soul Extreme Telegram Bot!\n\nYou are currently *not 
        registered* as a member. Please click on the button to register for Soul Extreme."""

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
    markup = telebot.util.quick_markup(
        {
            "Register": {
                "url": "https://forms.gle/LwbPKfyENvbnCkN28",
                "callback_data": {
                    "command": os.path.basename(__file__).removesuffix(".py"),
                    "chat_id": chat_id,
                    "step": "registration",
                },
            }
        },
        row_width=1,
    )

    return markup


def handle_callback_query(bot: telebot.TeleBot, call):
    """
    POST chat_id to google form. The chat_id field on the form is hidden from the user.
    """
    form_url = "https://forms.gle/LwbPKfyENvbnCkN28"
    chat_id = call.data["chat_id"]

    # response = requests.post(form_url, json={
    #     "chat_id": chat_id
    # })
    #
    # if response.status_code != 200:
    #     print("Error sending data to Google Form")
    bot.send_message(chat_id, "Need to POST")
