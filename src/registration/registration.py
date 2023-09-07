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
from src.resources.table_data.tables                        import Tables, TABLE_KEYS
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
            print("Registration Success")
            profile_created = create_profile(chat_id)

            if profile_created is True:
                print("Profile Created!")
                # se_telegram_bot.send_message(
                #     chat_id=chat_id,
                #     text=f"Thank you for registering for Soul Extreme! How may I assist you?",
                # )

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

    :param form_data: The form data from the submitted registration form
    :returns True if registration succeeds. False if it fails.
    """

    personal_particulars_table = DynamoDBTable(
        Tables.PERSONAL_PARTICULARS.value,
        TABLE_KEYS[Tables.PERSONAL_PARTICULARS]
    )

    var_map = {
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

    item = {}
    for field, value in form_data.items():
        db_field = var_map[field].value
        item[db_field] = value

        # Special Handling for genre which needs to be mapped to an enum
        if db_field == PersonalParticularsFields.GENRE.value:
            genre_value = ", ".join(value)
            item[db_field] = genre_value

    # Convert certain fields
    chat_id = item[PersonalParticularsFields.CHAT_ID.value]
    item[PersonalParticularsFields.CHAT_ID.value] = int(chat_id)

    match item[PersonalParticularsFields.STUDENT_STATUS.value]:
        case "Student":
            item[PersonalParticularsFields.STUDENT_STATUS.value] = True

            year_string = item[PersonalParticularsFields.YEAR.value]
            item[PersonalParticularsFields.YEAR.value] = int(year_string)

            graduation_year_string = item[PersonalParticularsFields.GRADUATION_YEAR.value]
            item[PersonalParticularsFields.GRADUATION_YEAR.value] = int(graduation_year_string)

        case "Alumni":
            item[PersonalParticularsFields.STUDENT_STATUS.value] = False

    try:
        personal_particulars_table.put_item(item)
        return True
    except Exception as error:
        print(error)
        return False


def create_profile(chat_id) -> bool:
    personal_particulars_table = DynamoDBTable(
        Tables.PERSONAL_PARTICULARS.value,
        TABLE_KEYS[Tables.PERSONAL_PARTICULARS]
    )
    member_profile_table = DynamoDBTable(
        Tables.MEMBER_PROFILE.value,
        TABLE_KEYS[Tables.MEMBER_PROFILE]
    )

    user = personal_particulars_table.get_item(chat_id)

    # Build a new member profile
    item = {
        MemberProfileFields.CHAT_ID.value: chat_id,
        MemberProfileFields.STUDENT_STATUS.value: bool(),
        MemberProfileFields.GENRE.value: user[PersonalParticularsFields.GENRE.value],
        MemberProfileFields.CREDITS.value: 0,
        MemberProfileFields.ADMIN.value: False
    }

    match user[PersonalParticularsFields.STUDENT_STATUS.value]:
        case "True":
            item[MemberProfileFields.STUDENT_STATUS.value] = True
        case "False":
            item[MemberProfileFields.STUDENT_STATUS.value] = False

    try:
        member_profile_table.put_item(item)
        return True
    except Exception as error:
        print(error)
        return False
