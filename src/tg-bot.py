"""
File        : tg-bot.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot.
"""

import logging
import json
import os

import telebot


# ======================================================================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), threaded=False)


def process_event(event):
    # Get telegram webhook json from event
    request_body_dict = json.loads(event["body"])
    # Parse updates from json
    update = telebot.types.Update.de_json(request_body_dict)
    # Run handlers and etc for updates
    bot.process_new_updates([update])


def handler(event, context):
    # Process event from aws and respond
    process_event(event)
    return {"statusCode": 200}


# Handle '/start' and '/help'
@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id

    bot.reply_to(
        message,
        f"Hi {chat_id}!",
    )
