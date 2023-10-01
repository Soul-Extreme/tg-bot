"""
File        : callback_helpers.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Helper methods for dealing with callback data
"""

from .conversation_state import ConversationState

# ========================================================================================


def pack_callback_data(command: str, chat_id: int, next_state: ConversationState):
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
