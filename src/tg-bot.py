"""
File        : tg-bot.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot.
"""

import logging
import os
import json

import telebot

# ======================================================================================================================

# Constants
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=False)


@bot.message_handlers(commands=['start'])
def start(message):
    """
    Handles the /start command
    """
    bot.reply_to(message, f'Hi {message.chat.id}!')


def handler(event, context):
    print(event)

    try:
        # de-jsons the request body
        update = telebot.types.Update.de_json(json.loads(event['body']))

        # run handlers for updates
        bot.process_new_updates([update])

        return {
            "statusCode": 200
        }

    except Exception as error:

        print(error)
        return {
            "statusCode": 200
        }
