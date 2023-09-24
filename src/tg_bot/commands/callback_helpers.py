"""
File        : callback_helpers.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Helper methods for dealing with callback data
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict

from src.resources.table_data.tables import CHAT_STATE_TABLE
from src.resources.table_data.table_fields import ChatStateFields

# ======================================================================================================================


class ConversationState(Enum):
    def __str__(self):
        return self.value


class CreditsState(str, ConversationState):
    CREDITS_MENU = "credits_menu"
    BUY_CREDITS = "buy_credits"
    PAY_INDIVIDUAL = "pay_individual"
    PAY_PACKAGE = "pay_package"
    INDIVIDUAL_X1 = "individual_x1"
    INDIVIDUAL_X2 = "individual_x2"


def pack_callback_data(
    command: str, chat_id: int, next_state: ConversationState
):
    """
    Packs the callback data for a conversation into one string.
    The total length of the string including separators must be under 64 bytes!

    :param command: The command where this conversation starts
    :param chat_id: The chat_id where this data originates from
    :param next_state: The next_state of the conversation
    :return: The packed callback data
    """
    callback_data = f"{command};{chat_id};{next_state}"
    if len(callback_data.encode("utf-8")) > 64:
        print("callback_data cannot be formed! Args are too long!")
        return ""

    return callback_data


def unpack_callback_data(callback_data: str):
    unpacked_dict = callback_data.split(";")
    command, chat_id, next_state = [i for i in unpacked_dict]

    data = {
        "command": command,
        "chat_id": int(chat_id),
        "next_state": next_state,
    }

    return data


def cache_conversation_state(command: str, chat_id: int, data: Dict = None):
    """
    Caches the conversation state into a DynamoDB Table.

    :param command: The command where this conversation starts
    :param chat_id: The chat_id where this data originates from
    :param data: A dictionary of custom data to store in JSON format.
    :return: The packed callback data
    """
    if data is None:
        data = {}

    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary!")

    time_in_48_hours = datetime.now() + timedelta(hours=48)

    chat_state_json = {
        ChatStateFields.COMMAND.value: command,
        ChatStateFields.CHAT_ID.value: chat_id,
        ChatStateFields.TTL.value: int(time_in_48_hours.timestamp()),
        "data": data,
    }

    try:
        CHAT_STATE_TABLE.put_item(json.dumps(chat_state_json))
    except Exception as error:
        print(error)
