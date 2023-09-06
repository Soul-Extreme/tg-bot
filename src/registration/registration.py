"""
File        : registration.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Entry point for the Telegram Bot Registration.
"""

import json
import os
import logging

import telebot

from src.resources.dynamodb_table import DynamoDBTable
from src.resources.table_names import Tables, TABLE_KEYS

# ======================================================================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

se_telegram_bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), threaded=False)


def handler(event, context):
    try:
        event_body = json.loads(event["body"])
        registration_status = register_member(event_body)

        if registration_status:
            name = (
                event_body["Preferred Name"]
                if event_body["Preferred Name"]
                else event_body["Full Name"]
            )
            se_telegram_bot.send_message(
                chat_id=int(event_body["User ID"]),
                text=f"Thank you for registering for Soul Extreme {name}! How may I assist you?",
            )

        return {"statusCode": 200}

    except Exception as error:
        print(error)
        return {"statusCode": 200}


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


def register_member(form_data) -> bool:
    """
    Parses the form_data and inserts into the personal-particulars database.
    A default member profile will also be created.

    :param form_data: The form data from the submitted registration form
    :returns True if registration succeeds. False if it fails.
    """

    personal_particulars_table = DynamoDBTable(
        Tables.PERSONAL_PARTICULARS.value, TABLE_KEYS[Tables.PERSONAL_PARTICULARS]
    )
    member_profile_table = DynamoDBTable(
        Tables.MEMBER_PROFILE.value, TABLE_KEYS[Tables.MEMBER_PROFILE]
    )

    # These are all hard-coded to match the ones in the form_data. If the form fields change, so must these!
    # Students have an extra set of fields to extract

    var_map = {
        "User ID": "chat_id",
        "Full Name": "full_name",
        "Preferred Name": "preferred_name",
        "Phone Number": "phone_number",
        "Telegram Handle": "telegram_handle",
        "Last 4 Characters of NRIC": "nric_last4",
        "Student ID": "student_id",
        "Cluster": "cluster",
        "Programme": "programme",
        "Year": "year",
        "Graduation Year": "graduation_year",
        "Emergency Contact Name": "emergency_contact_name",
        "Emergency Contact Relation": "emergency_contact_relation",
        "Emergency Contact Number": "emergency_contact_number",
        "Which genre(s) are you registering for?": "genre",
        "Shirt Size": "shirt_size",
        "Jacket Size": "jacket_size",
    }

    personal_particulars_item = {}
    for field, value in form_data:
        personal_particulars_item[var_map[field]] = value

    # Convert certain fields to numbers (int). Only applies to students!
    if personal_particulars_item["student_status"] == "Student":
        personal_particulars_item["student_id"] = int(
            personal_particulars_item["student_id"]
        )
        personal_particulars_item["year"] = int(personal_particulars_item["year"])
        personal_particulars_item["graduation_year"] = int(
            personal_particulars_item["graduation_year"]
        )

    # Create a member profile
    member_profile_item = {
        "chat_id": int(personal_particulars_item["chat_id"]),
        "name": (
            personal_particulars_item["preferred_name"]
            if personal_particulars_item["preferred_name"]
            else personal_particulars_item["full_name"]
        ),
        "genre": personal_particulars_item["genre"],
        "credits": 0,
    }

    try:
        personal_particulars_table.put_item(personal_particulars_item)
        member_profile_table.put_item(member_profile_item)

        return True
    except Exception as error:
        print(error)
        return False
