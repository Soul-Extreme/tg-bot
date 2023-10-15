"""
File        : credits.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /credits command for the SE Telegram Bot
"""

import json
import os
from datetime import datetime, timedelta

import telebot
from telebot.types import LabeledPrice

from src.tg_bot.conversation_state import ConversationState, cache_conversation_state
from src.tg_bot.markup_helpers import generate_button_definition, generate_markup
from src.resources.table_data.table_fields import MemberProfileFields
from src.resources.table_data.tables import (
    PERSONAL_PARTICULARS_TABLE,
    MEMBER_PROFILE_TABLE,
    CHAT_STATE_TABLE,
)

# ========================================================================================
# Variables
# ========================================================================================

CLASS_PRICING = {
    "Student": {"Individual": 10, "Package": 25},
    "Alumni": {"Individual": 13, "Package": 35},
}

COMMAND = "credits"

STRIPE_TOKEN = os.getenv("STRIPE_TOKEN")

# ========================================================================================
# State Graph
# ========================================================================================


class CreditsState(ConversationState):
    CREDITS_MENU = "credits_menu"
    BUY_CREDITS = "buy_credits"
    PAY_INDIVIDUAL = "pay_individual"
    PAY_PACKAGE = "pay_package"
    INDIVIDUAL_X1 = "individual_x1"
    INDIVIDUAL_X2 = "individual_x2"


CreditsState.CREDITS_MENU.next_states = [CreditsState.BUY_CREDITS]

CreditsState.BUY_CREDITS.prev_state = CreditsState.CREDITS_MENU
CreditsState.BUY_CREDITS.next_states = [
    CreditsState.PAY_INDIVIDUAL,
    CreditsState.PAY_PACKAGE,
]

CreditsState.PAY_INDIVIDUAL.prev_state = CreditsState.BUY_CREDITS
CreditsState.PAY_INDIVIDUAL.next_states = [
    CreditsState.INDIVIDUAL_X1,
    CreditsState.INDIVIDUAL_X2,
]

CreditsState.PAY_PACKAGE.prev_state = CreditsState.BUY_CREDITS
CreditsState.PAY_PACKAGE.next_states = [CreditsState.CREDITS_MENU]

CreditsState.INDIVIDUAL_X1.prev_state = CreditsState.PAY_INDIVIDUAL
CreditsState.INDIVIDUAL_X1.next_states = [CreditsState.CREDITS_MENU]

CreditsState.INDIVIDUAL_X2.prev_state = CreditsState.PAY_INDIVIDUAL
CreditsState.INDIVIDUAL_X2.next_states = [CreditsState.CREDITS_MENU]


# ========================================================================================
# Methods
# ========================================================================================


def command_credits(bot: telebot.TeleBot, message):
    """
    Displays an inline keyboard with the number of credits and the option to
    purchase more.

    :param bot: The telebot invoking this command.
    :param message: The message received from the telegram server
    """

    chat_id = message.chat.id
    user_particulars = PERSONAL_PARTICULARS_TABLE.get_item(chat_id)

    if not user_particulars:
        missing_user_message = (
            "Sorry 😥 your profile was not found within our database!\n"
            "Please run the /start command to register with us!"
        )

        bot.send_message(chat_id=chat_id, text=missing_user_message)

    else:
        state_handler(bot, chat_id, CreditsState.CREDITS_MENU)


def callback_query_credits(bot, data):
    chat_id = data["chat_id"]
    next_state = data["next_state"]

    # Delete previous message then send new message
    state_json = CHAT_STATE_TABLE.get_item(COMMAND, chat_id)

    if bool(state_json):
        conversation_state = json.loads(state_json["data"])
        bot.delete_message(chat_id, conversation_state["message_id"])

    state_handler(bot, chat_id, CreditsState(next_state))


# ==============================================================================
# HELPERS
# ==============================================================================


def state_handler(bot, chat_id, conversation_state: CreditsState):
    cache = True

    match conversation_state:
        case CreditsState.CREDITS_MENU:
            user_profile = MEMBER_PROFILE_TABLE.get_item(chat_id)

            name = user_profile[MemberProfileFields.NAME.value]
            num_credits = user_profile[MemberProfileFields.CREDITS.value]

            message_text = (
                f"{name}'s Remaining Class Credits:\n"
                f"<code>{num_credits}</code>\n\n"
                f"Press on the <b>Buy Class Credits</b> button below to purchase "
                f"more class credits!"
            )

            button_definitions = generate_button_definition(
                ["Buy Credits"], COMMAND, chat_id, conversation_state
            )

            message = bot.send_message(
                chat_id=chat_id,
                text=message_text,
                parse_mode="HTML",
                reply_markup=generate_markup(button_definitions, row_width=1),
            )

        case CreditsState.BUY_CREDITS:
            user_profile = MEMBER_PROFILE_TABLE.get_item(chat_id)

            student_status = (
                "Student"
                if user_profile[MemberProfileFields.STUDENT_STATUS.value]
                else "Alumni"
            )

            individual_price = CLASS_PRICING[student_status]["Individual"]
            package_price = CLASS_PRICING[student_status]["Package"]

            message_text = (
                f"How many class credits would you like to buy?\n\n"
                f"<b>[{student_status} Pricing]</b>\n"
                f"Individual: ${individual_price} per class credit\n"
                f"Package: ${package_price} for 3 class credits"
            )

            button_definitions = generate_button_definition(
                ["Individual", "Package"], COMMAND, chat_id, conversation_state, True
            )

            message = bot.send_message(
                chat_id=chat_id,
                text=message_text,
                parse_mode="HTML",
                reply_markup=generate_markup(button_definitions, row_width=1),
            )

        case CreditsState.PAY_PACKAGE:
            user_profile = MEMBER_PROFILE_TABLE.get_item(chat_id)

            student_status = (
                "Student"
                if user_profile[MemberProfileFields.STUDENT_STATUS.value]
                else "Alumni"
            )

            price = CLASS_PRICING[student_status]["Package"]

            prices = [LabeledPrice("3 Class Credits", price * 100)]

            bot.send_invoice(
                chat_id=chat_id,
                title=f"{student_status} Package Class Credits",
                description=f"Please make a payment of S${price} for 3 class credits!",
                invoice_payload=f"{student_status} Package Class Credits",
                provider_token=STRIPE_TOKEN,
                currency="sgd",
                prices=prices,
                is_flexible=False,
            )

            cache = False

        case CreditsState.PAY_INDIVIDUAL:
            user_profile = MEMBER_PROFILE_TABLE.get_item(chat_id)

            student_status = (
                "Student"
                if user_profile[MemberProfileFields.STUDENT_STATUS.value]
                else "Alumni"
            )

            individual_price = CLASS_PRICING[student_status]["Individual"]

            message_text = (
                f"How many class credits would you like to buy?\n\n"
                f"<b>[{student_status} Pricing]</b>\n"
                f"${individual_price} per class credit"
            )

            button_definitions = generate_button_definition(
                ["1", "2"], COMMAND, chat_id, conversation_state, True
            )

            message = bot.send_message(
                chat_id=chat_id,
                text=message_text,
                parse_mode="HTML",
                reply_markup=generate_markup(button_definitions, row_width=2),
            )

        case CreditsState.INDIVIDUAL_X1:
            bot.send_message(chat_id=chat_id, text="Paying 1")
            return

        case CreditsState.INDIVIDUAL_X2:
            bot.send_message(chat_id=chat_id, text="Paying 2")
            return

    if cache:
        cache_data = {
            "state": conversation_state.value,
            "message_id": message.id,
        }
        cache_conversation_state(COMMAND, chat_id, cache_data)
