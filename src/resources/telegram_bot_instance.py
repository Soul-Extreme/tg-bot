"""
File        : telegram_bot_instance.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Instance for the SE Telegram Bot.
"""

import os

import telebot

# ======================================================================================================================

SE_TELEGRAM_BOT = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'), threaded=False)
