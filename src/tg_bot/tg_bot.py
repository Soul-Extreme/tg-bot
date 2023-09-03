"""
File        : tg_bot.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot.
"""

import logging
import os
import json

import telebot

from .commands.collections import COMMAND_LIST, COMMAND_DICT

# ======================================================================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

se_telegram_bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), threaded=False)


def handler(event, context):
    print(event)

    try:
        # de-jsons the request body
        update = telebot.types.Update.de_json(json.loads(event["body"]))
        se_telegram_bot.process_new_updates([update])

        return {"statusCode": 200}

    except Exception as error:
        logger.error(error)
        return {"statusCode": 200}


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


@se_telegram_bot.message_handler(commands=COMMAND_LIST)
def dispatcher(message):
    """
    Dispatches commands message to their respective handlers

    :param message: The incoming message from the telegram server
    """

    command = message.text.removeprefix("/")
    COMMAND_DICT[command](se_telegram_bot, message)
