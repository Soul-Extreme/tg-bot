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


def handler(event, context):
    print(os.getenv("TELEGRAM_BOT_TOKEN"))
    return {"statusCode": 200}
