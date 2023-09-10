"""
File        : start.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Executes the /start command for the SE Telegram Bot
"""

import telebot

from src.resources.dynamodb_table                           import DynamoDBTable
from src.resources.table_data.tables                        import PERSONAL_PARTICULARS_TABLE
from src.resources.table_data.personal_particulars_table    import PersonalParticularsFields


# ======================================================================================================================


def command_start(bot: telebot.TeleBot, message):
    """
    Runs through the /start command flow:

    1. Checks for user in DynamoDB Personal Particulars Table
    2a. If user doesn't exist; Prompt Registration through inline keyboard
    2b. If user exists; greet

    :param bot: The telebot invoking this command.
    :param message: The message received from the telegram server
    """

    chat_id = message.chat.id
    user    = PERSONAL_PARTICULARS_TABLE.get_item(chat_id)

    if not user:
        # If user cannot be found, we prompt registration
        registration_prompt_message = (
            f"Welcome to the Soul Extreme Telegram Bot!\n\nYour <b>user ID</b> is:\n<code>{chat_id}</code>\nCopy and "
            f"paste this into the user ID field on the registration form as shown in the attached image. (Tap on the "
            f"ID to copy it)\n\nPlease click on the <b>Register</b> button below to register for Soul Extreme.\n\nYou "
            f"should receive a confirmation message once you've registered. If you do not, please contact a committee "
            f"member."
        )

        bot.send_photo(
            chat_id     =chat_id,
            photo       ="https://i.imgur.com/xNSx2QD.png",
            caption     =registration_prompt_message,
            parse_mode  ="HTML",
            reply_markup=gen_registration_keyboard_markup(),
        )

    else:
        name = user[PersonalParticularsFields.FULL_NAME.value]

        if user[PersonalParticularsFields.PREFERRED_NAME.value]:
            name = user[PersonalParticularsFields.PREFERRED_NAME.value]

        bot.send_message(chat_id, f"Welcome back {name}! How may I assist you?")


# ======================================================================================================================
# HELPERS
# ======================================================================================================================


def gen_registration_keyboard_markup():
    """
    Creates the inline keyboard to prompt Registration

    :param chat_id: The chat_id that will be POSTed to the Google form for registration
    :return: The markup for the inline keyboard
    """

    # The values in each button for an inline keyboard will only execute the first kwarg. Multiple is not supported!
    markup = telebot.util.quick_markup(
        {"Register": {"url": "https://forms.gle/ndRGqt3yM8W5QLd26"}},
        row_width=1,
    )

    return markup
