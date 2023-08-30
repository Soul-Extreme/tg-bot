"""
File        : set_webhook.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Runner for setting the webhook during the deployment workflow.
"""

import requests
import os

# ======================================================================================================================

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
apigw_url = os.getenv("TG_BOT_ENDPOINT")

response = requests.get(
    f"https://api.telegram.org/bot{bot_token}/setWebhook?url={apigw_url}"
)

print(response)
