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
lambda_url = os.getenv("AWS_LAMBDA_TGBOT_ENDPOINT")

response = requests.get(
    f"https://api.telegram.org/bot{bot_token}/setWebhook?url={lambda_url}"
)

print(response)
