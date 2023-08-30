"""
File        : tg-boy.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot.
"""

import json
import os
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
)

# ======================================================================================================================

tg_bot_app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=user_chat_id, text=f"Hello {user_chat_id}!")


async def main(event, context):
    tg_bot_app.add_handler(CommandHandler("start", start))

    try:
        await tg_bot_app.initialize()
        await tg_bot_app.process_update(
            Update.de_json(json.loads(event["body"]), tg_bot_app.bot)
        )

        return {"statusCode": 200, "body": "Success"}
    except Exception as error:
        return {"statusCode": 500, "body": "Failure"}


def handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))
