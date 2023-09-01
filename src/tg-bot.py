"""
File        : tg-bot.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot.
"""

import json


# ======================================================================================================================

def handler(event, context):
    print(event)

    try:
        body = json.loads(event['body'])
        print(body)

        return {"statusCode": 200}
    except Exception as error:
        print(error)

        return {"statusCode": 200}
