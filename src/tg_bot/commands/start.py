"""
File        : start.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /start command for the SE Telegram Bot
"""

import telebot


# ======================================================================================================================

def start_command(bot: telebot.TeleBot, message):
    """
    Runs through the /start command flow:

    1. Checks for user in DynamoDB Personal Particulars Table
    2a. If user doesn't exist; Prompt Registration through inline keyboard
    2b. If user exists; greet
    """

    # For testing, we just echo back the chat it
    bot.send_message(message.chat.id, f"Hi {message.chat.id}!")
