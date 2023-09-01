"""
File        : tg_bot.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot.
"""

import logging
import os
import json

from .commands.command_list import command_list, command_dict

import telebot

# ======================================================================================================================

# Constants
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up any necessary logging
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Create telegram bot
se_telegram_bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)


def handler(event, context):
    print(event)

    try:
        # de-jsons the request body
        update = telebot.types.Update.de_json(json.loads(event['body']))
        se_telegram_bot.process_new_updates([update])

        return {
            "statusCode": 200
        }

    except Exception as error:
        logger.error(error)
        return {
            "statusCode": 200
        }


# ======================================================================================================================
# HELPERS
# ======================================================================================================================

@se_telegram_bot.message_handler(commands=command_list)
def dispatcher(message):
    """
    Dispatches messages to the appropriate handler methods
    """

    # Remove '/' prefix from incoming message
    command = message.text.removeprefix('/')
    command_dict[command](se_telegram_bot, message)
