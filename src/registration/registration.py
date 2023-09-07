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

from src.resources.dynamodb_table                           import DynamoDBTable
from src.resources.table_data.tables                        import PERSONAL_PARTICULARS_TABLE, MEMBER_PROFILE_TABLE
from src.resources.table_data.personal_particulars_table    import PersonalParticularsFields
from src.resources.table_data.member_profile_table          import MemberProfileFields

# ======================================================================================================================

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

se_telegram_bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), threaded=False)


def handler(event, context):
    try:
        event_body = json.loads(event["body"])

        registration_status = register_member(event_body)
        chat_id = int(event_body["User ID"])

        if registration_status is True:
            se_telegram_bot.send_message(
                chat_id=chat_id,
                text=f"Thank you for registering for Soul Extreme! How may I assist you?",
                allow_sending_without_reply=True
            )

        return {
            "statusCode": 200
        }

    except Exception as error:
        print(error)
        return {
            "statusCode": 200
        }


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


def register_member(form_data) -> bool:
    """
    Parses the form_data and
    1. Inserts into the personal-particulars table.
    2. Builds a new member profile and inserts it into the member-profile table.

    :param form_data: The form data from the submitted registration form.
    :returns True if registration succeeds. False if it fails.
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

    personal_particulars_state = False
    member_profile_state = False

    personal_particulars_item = {}
    for field, value in form_data.items():
        personal_profile_field = personal_particulars_key_map[field].value
        personal_particulars_item[personal_profile_field] = value

        # Special Handling for genre which needs to be mapped to an enum
        if personal_profile_field == PersonalParticularsFields.GENRE.value:
            genre_value = ", ".join(value)
            personal_particulars_item[personal_profile_field] = genre_value

    # Convert certain fields to their correct types
    chat_id = personal_particulars_item[PersonalParticularsFields.CHAT_ID.value]
    personal_particulars_item[PersonalParticularsFields.CHAT_ID.value] = int(chat_id)

    match personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS.value]:
        case "Student":
            personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS.value] = True

            year_string = personal_particulars_item[PersonalParticularsFields.YEAR.value]
            personal_particulars_item[PersonalParticularsFields.YEAR.value] = int(year_string)

            graduation_year_string = personal_particulars_item[PersonalParticularsFields.GRADUATION_YEAR.value]
            personal_particulars_item[PersonalParticularsFields.GRADUATION_YEAR.value] = int(graduation_year_string)

        case "Alumni":
            personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS.value] = False

    try:
        personal_particulars_state = PERSONAL_PARTICULARS_TABLE.put_item(personal_particulars_item)
        if personal_particulars_state is True:
            print(f"Registration success for {chat_id}!")
    except Exception as error:
        print(error)
        return False

    # Create member profile
    member_profile_item = {
        MemberProfileFields.CREDITS.value: 0,
        MemberProfileFields.ADMIN.value: False,
        MemberProfileFields.CHAT_ID.value: (
            personal_particulars_item[PersonalParticularsFields.CHAT_ID.value]
        ),
        MemberProfileFields.STUDENT_STATUS.value: (
            personal_particulars_item[PersonalParticularsFields.STUDENT_STATUS.value]
        ),
        MemberProfileFields.GENRE.value: (
            personal_particulars_item[PersonalParticularsFields.GENRE.value]
        )
    }

    try:
        member_profile_state = MEMBER_PROFILE_TABLE.put_item(member_profile_item)
        if member_profile_state is True:
            print(f"Member Profile Creation success for {chat_id}!")
    except Exception as error:
        print(error)
        return False

    return True
