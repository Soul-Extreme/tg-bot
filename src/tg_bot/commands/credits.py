"""
File        : credits.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /credits command for the SE Telegram Bot
"""

import json
from enum import Enum

import telebot

from src.resources.table_data.tables import (
    PERSONAL_PARTICULARS_TABLE,
    MEMBER_PROFILE_TABLE,
)
from src.resources.table_data.personal_particulars_table import PersonalParticularsFields
from src.resources.table_data.member_profile_table import MemberProfileFields

# ======================================================================================================================


def command_credits(bot: telebot.TeleBot, message):
    """
    Displays an inline keyboard with the number of credits and the option to purchase more.

    :param bot: The telebot invoking this command.
    :param message: The message received from the telegram server
    """

    chat_id = message.chat.id
    user_profile = MEMBER_PROFILE_TABLE.get_item(chat_id)
    user_particulars = PERSONAL_PARTICULARS_TABLE.get_item(chat_id)

    if not user_profile:
        missing_user_message = (
            "Sorry 😥 your profile was not found within our database!\nPlease run the /start "
            "command to register with us!"
        )

        bot.send_message(chat_id=chat_id, text=missing_user_message)

    else:
        name = user_particulars[PersonalParticularsFields.FULL_NAME.value]

        if user_particulars[PersonalParticularsFields.PREFERRED_NAME.value]:
            name = user_particulars[PersonalParticularsFields.PREFERRED_NAME.value]

        num_credits = user_profile[MemberProfileFields.CREDITS.value]
        student_status = "Student" if user_profile[MemberProfileFields.STUDENT_STATUS.value] else "Alumni"

        credits_info_message = (
            f"Member Name: {name}\nStudent Status: {student_status}\n\n "
            f"Remaining Credits:\n<code>{num_credits}</code>\n\n"
            f"Press on the <b>Buy Credits</b> button below to purchase more credits!"
        )

        bot.send_message(
            chat_id=chat_id,
            text=credits_info_message,
            parse_mode="HTML",
            reply_markup=credits_menu_markup(chat_id),
        )


def credits_menu_markup(chat_id):
    """
    Creates the inline keyboard for the credits menu

    :param chat_id: The chat_id where this inline keyboard is created.
    :return: The markup for the inline keyboard
    """

    # The values in each button for an inline keyboard will only execute the first kwarg. Multiple is not supported!
    buy_credits_callback_data = {"command": "credits", "step": Steps.BUY_CREDITS, "chat_id": chat_id}

    markup = telebot.util.quick_markup(
        {"Buy Credits": {"callback_data": json.dumps(buy_credits_callback_data)}},
        row_width=1,
    )

    return markup


def callback_query_credits(bot, data):
    match data["step"]:
        case Steps.BUY_CREDITS:
            payment_menu(bot, data["chat_id"])


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


class Steps(str, Enum):
    BUY_CREDITS = "buy_credits"
    PAY = "pay"


def payment_menu(bot, chat_id):
    bot.send_message(chat_id=chat_id, text="Payment test!")
