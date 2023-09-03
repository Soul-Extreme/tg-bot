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

# ======================================================================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

SE_TELEGRAM_BOT = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'), threaded=False)


def handler(event, context):
    print(event)

    try:
        # de-jsons the request body
        update = telebot.types.Update.de_json(json.loads(event['body']))
        SE_TELEGRAM_BOT.process_new_updates([update])

        return {
            "statusCode": 200
        }

    except Exception as error:
        logger.error(error)
        return {
            "statusCode": 200
        }
