"""
File        : register.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /start command for the SE Telegram Bot
"""

import telebot

from src.resources.table_data.tables import PERSONAL_PARTICULARS_TABLE
from src.resources.table_data.table_fields import PersonalParticularsFields


# ========================================================================================
# Variables
# ========================================================================================

COMMAND = "register"

# ========================================================================================
# Methods
# ========================================================================================


def command_register(bot: telebot.TeleBot, message):
    """
    Runs through the /register command flow:

    1. Checks for user in DynamoDB Personal Particulars Table
    2a. If user doesn't exist; Prompt Registration through inline keyboard
    2b. If user exists; greet

    :param bot: The telebot invoking this command.
    :param message: The message received from the telegram server
    """

    chat_id = message.chat.id
    user = PERSONAL_PARTICULARS_TABLE.get_item(chat_id)

    if not user:
        # If user cannot be found, we prompt registration
        registration_prompt_message = (
            f"Welcome to the Soul Extreme Telegram Bot!\n\n"
            f"Your <b>user ID</b> is:\n"
            f"<code>{chat_id}</code>\n\n"
            f"Copy and paste this into the user ID field on the registration "
            f"form as shown in the attached image.\n"
            f"(Tap on the ID to copy it)\n\n"
            f"Please click on the <b>Register</b> button below to register for Soul Extreme.\n\n"
            f"You should receive a confirmation message once you've registered."
            f"If you do not, please contact a committee member."
        )

        markup = telebot.util.quick_markup(
            {"Register": {"url": "https://forms.gle/ndRGqt3yM8W5QLd26"}},
            row_width=1,
        )

        bot.send_photo(
            chat_id=chat_id,
            photo="https://i.imgur.com/xNSx2QD.png",
            caption=registration_prompt_message,
            parse_mode="HTML",
            reply_markup=markup,
        )

    else:
        name = user[PersonalParticularsFields.FULL_NAME.value]

        if user[PersonalParticularsFields.PREFERRED_NAME.value]:
            name = user[PersonalParticularsFields.PREFERRED_NAME.value]

        bot.send_message(chat_id, f"Welcome back {name}! How may I assist you?")
