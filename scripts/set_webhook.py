"""
File        : set_webhook.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description :   Script for setting the webhook for the telegram bot through a GitHub action. There should not be a need
                to run this often.
"""

import requests
import os

# ======================================================================================================================

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
apigw_endpoint = os.getenv('TG_BOT_ENDPOINT')

try:
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/setWebhook', json={
        "url": apigw_endpoint
    })

    print(f"""Status Code: {response.status_code} \n
        {response.json}
    """)

except Exception as error:
    print(error)
