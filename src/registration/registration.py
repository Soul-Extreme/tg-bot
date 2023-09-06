"""
File        : registration.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot Registration.
"""

import json
import os

# ======================================================================================================================


def handler(event, context):
    try:
        event_body = json.loads(event["body"])
        print(event_body)

    except Exception as error:
        print(error)
        return {"statusCode": 200}


# ======================================================================================================================
# HELPERS
# ======================================================================================================================
