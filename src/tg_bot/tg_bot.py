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

from .commands.callback_helpers import unpack_callback_data
from .commands.collections import COMMAND_MAP, CALLBACK_QUERY_MAP

# ======================================================================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

se_telegram_bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), threaded=False)

command_list = ["start", "credits"]


def handler(event, context):
    print(event)

    try:
        update = telebot.types.Update.de_json(json.loads(event["body"]))
        se_telegram_bot.process_new_updates([update])

        return {"statusCode": 200}

    except Exception as error:
        print(error)

        return {"statusCode": 200}


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


@se_telegram_bot.message_handler(commands=command_list)
def command_dispatch(message):
    """
    Dispatches commands message to their respective handlers
    """

    command = message.text.removeprefix("/")
    COMMAND_MAP[command](se_telegram_bot, message)


@se_telegram_bot.callback_query_handler(func=lambda call: True)
def callback_dispatch(call):
    """
    Dispatches callback queries from inline keyboard buttons to their respective handlers
    """

    data = unpack_callback_data(call.data)
    CALLBACK_QUERY_MAP[data["command"]](se_telegram_bot, data)
