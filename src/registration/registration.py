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

from src.resources.table_data.tables import (
    PERSONAL_PARTICULARS_TABLE,
    MEMBER_PROFILE_TABLE,
)
from src.resources.table_data.table_fields import (
    PersonalParticularsFields,
    MemberProfileFields,
)

# ==============================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

se_telegram_bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), threaded=False)


def handler(event, context):
    try:
        event_body = json.loads(event["body"])

        registration_status = register_member(event_body)
        chat_id = int(event_body["User ID"])

        if registration_status is True:
            name = (
                event_body["Preferred Name"]
                if event_body["Preferred Name"]
                else event_body["Full Name"]
            )

            se_telegram_bot.send_message(
                chat_id=chat_id,
                text=f"Thank you {name} for registering for Soul Extreme! "
                f"How may I assist you?",
                disable_notification=False,
            )

        return {"statusCode": 200}

    except Exception as error:
        print(error)
        return {"statusCode": 200}


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


def register_member(form_data):
    """
    Parses the form_data and
    1. Inserts into the Personal Particulars table.
    2. Builds a new member profile and inserts it into the Member Profile table.

    :param form_data: The form data from the submitted registration form.
    :return: True if
    """
    personal_particulars_key_map = {
        "User ID": PersonalParticularsFields.CHAT_ID,
        "Full Name": PersonalParticularsFields.FULL_NAME,
        "Preferred Name": PersonalParticularsFields.PREFERRED_NAME,
        "Phone Number": PersonalParticularsFields.PHONE_NUMBER,
        "Telegram Handle": PersonalParticularsFields.TELEGRAM_HANDLE,
        "Last 4 Characters of NRIC": PersonalParticularsFields.NRIC_LAST4,
        "Student Status": PersonalParticularsFields.STUDENT_STATUS,
        "Student ID": PersonalParticularsFields.STUDENT_ID,
        "Cluster": PersonalParticularsFields.CLUSTER,
        "Program": PersonalParticularsFields.PROGRAMME,
        "Year": PersonalParticularsFields.YEAR,
        "Graduation Year": PersonalParticularsFields.GRADUATION_YEAR,
        "Emergency Contact Name": PersonalParticularsFields.EMERGENCY_CONTACT_NAME,
        "Emergency Contact Relation": PersonalParticularsFields.EMERGENCY_CONTACT_RELATION,
        "Emergency Contact Number": PersonalParticularsFields.EMERGENCY_CONTACT_NUMBER,
        "Which genre(s) are you registering for?": PersonalParticularsFields.GENRE,
        "Shirt Size": PersonalParticularsFields.SHIRT_SIZE,
        "Jacket Size": PersonalParticularsFields.JACKET_SIZE,
    }

    personal_particulars_item = {}
    for field, value in form_data.items():
        table_field = personal_particulars_key_map[field].value
        personal_particulars_item[table_field] = value

        # Special Handling for genre which needs to be mapped to an enum
        if table_field == PersonalParticularsFields.GENRE:
            genre_value = ", ".join(value)
            personal_particulars_item[table_field] = genre_value

    # Convert certain fields to their correct types
    chat_id = personal_particulars_item[PersonalParticularsFields.CHAT_ID]
    personal_particulars_item[PersonalParticularsFields.CHAT_ID] = int(chat_id)

    match personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS]:
        case "Student":
            personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS] = True

            year = personal_particulars_item[PersonalParticularsFields.YEAR]
            personal_particulars_item[PersonalParticularsFields.YEAR] = int(year)

            graduation_year = personal_particulars_item[
                PersonalParticularsFields.GRADUATION_YEAR
            ]
            personal_particulars_item[PersonalParticularsFields.GRADUATION_YEAR] = int(
                graduation_year
            )

        case "Alumni":
            personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS] = False

    try:
        personal_particulars_state = PERSONAL_PARTICULARS_TABLE.put_item(
            personal_particulars_item
        )
        if personal_particulars_state is True:
            print(f"Registration success for {chat_id}!")
    except Exception as error:
        print(error)
        return False

    # Create member profile
    student_status = personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS]
    genre = personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS]
    name = personal_particulars_item[PersonalParticularsFields.FULL_NAME]

    if personal_particulars_item.get(PersonalParticularsFields.PREFERRED_NAME):
        name = personal_particulars_item[PersonalParticularsFields.PREFERRED_NAME]

    member_profile_item = {
        MemberProfileFields.CREDITS: 0,
        MemberProfileFields.ADMIN: False,
        MemberProfileFields.CHAT_ID: int(chat_id),
        MemberProfileFields.NAME: name,
        MemberProfileFields.STUDENT_STATUS: student_status,
        MemberProfileFields.GENRE: genre,
    }

    try:
        member_profile_state = MEMBER_PROFILE_TABLE.put_item(member_profile_item)
        if member_profile_state is True:
            print(f"Member Profile Creation success for {chat_id}!")
    except Exception as error:
        print(error)
        return False

    return True
