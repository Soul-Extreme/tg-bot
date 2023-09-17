"""
File        : credits.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /credits command for the SE Telegram Bot
"""

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

        credits_info_message = (
            f"{name}'s Remaining Credits:\n<code>{num_credits}</code>\n\n"
            f"Press on the <b>Buy Credits</b> button below to purchase more credits!"
        )

        bot.send_message(
            chat_id=chat_id,
            text=credits_info_message,
            parse_mode="HTML",
            reply_markup=credits_menu_markup(chat_id, message.id),
        )


def callback_query_credits(bot, data):
    chat_id = int(data["chat_id"])
    user = MEMBER_PROFILE_TABLE.get_item(chat_id)

    match data["step"]:
        case Steps.BUY_CREDITS:
            student_status = user[MemberProfileFields.STUDENT_STATUS.value]

            prorated_amount = 10 if student_status else 13
            pack_amount = 25 if student_status else 35

            student_status_string = "Student" if student_status else "Alumni"

            payment_options_message = (
                f"Please select your purchase option below\n\n"
                f"[{student_status_string}]\n"
                f"<code><b>Credits   Price</b></code>\n"
                f"<code>1         {prorated_amount}</code>\n"
                f"<code>3         {pack_amount}</code>\n\n"
                f"Terms and Conditions: /payment_t&c"
            )

            bot.send_message(
                chat_id=chat_id,
                text=payment_options_message,
                parse_mode="HTML",
                reply_markup=payment_menu_markup(chat_id, int(data["message_id"])),
            )
        case Steps.PAY_PRORATE:
            bot.send_message(chat_id=chat_id, text="Paying Pro-rated")
        case Steps.PAY_PACKAGE:
            bot.send_message(chat_id=chat_id, text="Paying Package")


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


class Steps(str, Enum):
    BUY_CREDITS = "buy_credits"
    PAY_PRORATE = "pay_prorate"
    PAY_PACKAGE = "pay_package"


def credits_menu_markup(chat_id: int, message_id: int):
    """
    Creates the inline keyboard for the credits menu

    :param chat_id: The chat_id where this inline keyboard is created.
    :param message_id: The message_id of this inline keyboard
    :return: The markup for the inline keyboard
    """

    buy_credits_callback_data = f"credits;{Steps.BUY_CREDITS.value};{chat_id};{message_id}"

    markup = telebot.util.quick_markup(
        {"Buy Credits": {"callback_data": buy_credits_callback_data}},
        row_width=1,
    )

    return markup


def payment_menu_markup(chat_id: int, message_id: int):
    """
    Creates an inline keyboard for the payment menu

    :param chat_id: The chat_id where this inline keyboard is created
    :param message_id: The message_id of this inline keyboard
    :return: The markup for the inline keyboard
    """

    payment_prorate_callback_data = f"credits;{Steps.PAY_PRORATE.value};{chat_id};{message_id}"
    payment_package_callback_data = f"credits;{Steps.PAY_PACKAGE.value};{chat_id};{message_id}"

    markup = telebot.util.quick_markup(
        {
            "1 credit": {"callback_data": payment_prorate_callback_data},
            "3 credits": {"callback_data": payment_package_callback_data},
        },
        row_width=1,
    )

    return markup
