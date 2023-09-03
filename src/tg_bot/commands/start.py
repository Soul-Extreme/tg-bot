"""
File        : start.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /start command for the SE Telegram Bot
"""

import telebot

from .dynamodb_table import DynamoDBTable
from .table_names import Tables, TABLE_KEYS


# ======================================================================================================================

def start_command(bot: telebot.TeleBot, message):
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
        bot.send_message(user_id, f"{user_id} needs to register!")
    else:
        bot.send_message(user_id, f"Welcome back {user_id}!")



