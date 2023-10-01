"""
File        : conversation_state.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Definitions for a conversation state as part of a simple graph.
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict
from enum import Enum

from src.resources.table_data.tables import CHAT_STATE_TABLE
from src.resources.table_data.table_fields import ChatStateFields

# ========================================================================================


class ConversationState(str, Enum):
    def __init__(self, _):
        self.prev_state = None
        self.next_states = []

    def __str__(self):
        return self.value


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

    chat_state_item = {
        ChatStateFields.COMMAND.value: command,
        ChatStateFields.CHAT_ID.value: chat_id,
        ChatStateFields.TTL.value: int(time_in_48_hours.timestamp()),
        "data": json.dumps(data),
    }

    try:
        CHAT_STATE_TABLE.put_item(chat_state_item)
    except Exception as error:
        print(error)


# TODO: Clear cached state
