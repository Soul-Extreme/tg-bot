"""
File        : credits.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /credits command for the SE Telegram Bot
"""

import json

import telebot

from .callback_helpers import (
    CreditsState,
    pack_callback_data,
    cache_conversation_state,
)
from src.resources.table_data.table_fields import (
    PersonalParticularsFields,
    MemberProfileFields,
)
from src.resources.table_data.tables import (
    PERSONAL_PARTICULARS_TABLE,
    MEMBER_PROFILE_TABLE,
    CHAT_STATE_TABLE,
)

# ==============================================================================

CLASS_PRICING = {
    "Student": {"Individual": 10, "Package": 25},
    "Alumni": {"Individual": 13, "Package": 35},
}

COMMAND = "credits"


def command_credits(bot: telebot.TeleBot, message):
    """
    Displays an inline keyboard with the number of credits and the option to
    purchase more.

    :param bot: The telebot invoking this command.
    :param message: The message received from the telegram server
    """

    chat_id = message.chat.id
    user_profile = MEMBER_PROFILE_TABLE.get_item(chat_id)
    user_particulars = PERSONAL_PARTICULARS_TABLE.get_item(chat_id)

    if not user_profile:
        missing_user_message = (
            "Sorry 😥 your profile was not found within our database!\n"
            "Please run the /start command to register with us!"
        )

        bot.send_message(chat_id=chat_id, text=missing_user_message)

    else:
        name = user_particulars[PersonalParticularsFields.FULL_NAME.value]

        if user_particulars[PersonalParticularsFields.PREFERRED_NAME.value]:
            name = user_particulars[
                PersonalParticularsFields.PREFERRED_NAME.value
            ]

        num_credits = user_profile[MemberProfileFields.CREDITS.value]

        credits_info_message = (
            f"{name}'s Remaining Class Credits:\n<code>{num_credits}</code>\n\n"
            f"Press on the <b>Buy Class Credits</b> button below to purchase "
            f"more class credits!"
        )

        message = bot.send_message(
            chat_id=chat_id,
            text=credits_info_message,
            parse_mode="HTML",
            reply_markup=credits_menu_markup(chat_id),
        )

        cache_data = {
            "step": CreditsState.CREDITS_MENU.value,
            "message_id": message.id,
        }
        cache_conversation_state(COMMAND, chat_id, cache_data)


def callback_query_credits(bot, data):
    chat_id = data["chat_id"]
    next_state = data["next_state"]

    # Delete previous message then send new message
    state_json = CHAT_STATE_TABLE.get_item(COMMAND, chat_id)

    if bool(state_json):
        conversation_state = json.loads(state_json)
        bot.delete_message(chat_id, conversation_state["data"]["message_id"])

    user = MEMBER_PROFILE_TABLE.get_item(chat_id)
    student_status = (
        "Student"
        if user[MemberProfileFields.STUDENT_STATUS.value]
        else "Alumni"
    )

    individual_price = CLASS_PRICING[student_status]["Individual"]
    package_price = CLASS_PRICING[student_status]["Package"]

    match next_state:
        case CreditsState.BUY_CREDITS:
            payment_options_message = (
                f"How many class credits would you like to buy?\n\n"
                f"<b>[{student_status} Pricing]</b>\n"
                f"Individual: ${individual_price} per class credit\n"
                f"Package: ${package_price} for 3 class credits"
            )

            message = bot.send_message(
                chat_id=chat_id,
                text=payment_options_message,
                parse_mode="HTML",
                reply_markup=payment_menu_markup(chat_id),
            )

            cache_data = {
                "step": CreditsState.BUY_CREDITS.value,
                "message_id": message.id,
            }
            cache_conversation_state(COMMAND, chat_id, cache_data)

        case CreditsState.PAY_INDIVIDUAL:
            payment_options_message = (
                f"How many class credits would you like to buy?\n\n"
                f"<b>[{student_status} Pricing]</b>\n"
                f"${individual_price} per class credit"
            )

            message = bot.send_message(
                chat_id=chat_id,
                text=payment_options_message,
                parse_mode="HTML",
                reply_markup=individual_payment_menu_markup(chat_id),
            )

            cache_data = {
                "step": CreditsState.BUY_CREDITS.value,
                "message_id": message.id,
            }
            cache_conversation_state("credits", chat_id, cache_data)

        case CreditsState.INDIVIDUAL_X1:
            bot.send_message(chat_id=chat_id, text="Buying 1 class credit")
        case CreditsState.INDIVIDUAL_X2:
            bot.send_message(chat_id=chat_id, text="Buying 2 class credits")
        case CreditsState.PAY_PACKAGE:
            bot.send_message(chat_id=chat_id, text="Paying Package")


# ==============================================================================
# HELPERS
# ==============================================================================


def credits_menu_markup(chat_id: int):
    markup = telebot.util.quick_markup(
        {
            "Buy Credits": {
                "callback_data": pack_callback_data(
                    COMMAND, chat_id, CreditsState.BUY_CREDITS
                )
            }
        },
        row_width=1,
    )

    return markup


def payment_menu_markup(chat_id: int):
    markup = telebot.util.quick_markup(
        {
            "Individual": {
                "callback_data": pack_callback_data(
                    COMMAND, chat_id, CreditsState.PAY_INDIVIDUAL
                )
            },
            "Package": {
                "callback_data": pack_callback_data(
                    COMMAND, chat_id, CreditsState.PAY_PACKAGE
                )
            },
        },
        row_width=1,
    )

    return markup


def individual_payment_menu_markup(chat_id: int):
    markup = telebot.util.quick_markup(
        {
            "1": {
                "callback_data": pack_callback_data(
                    COMMAND, chat_id, CreditsState.INDIVIDUAL_X1
                )
            },
            "2": {
                "callback_data": pack_callback_data(
                    COMMAND, chat_id, CreditsState.INDIVIDUAL_X2
                )
            },
        },
        row_width=2,
    )

    return markup
