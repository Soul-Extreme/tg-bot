"""
File        : callback_helpers.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Helper methods for dealing with callback data
"""

from .collections import Step, CALLBACK_DATA

# ======================================================================================================================


def pack_callback_data(command: str, step: Step, chat_id: int, message_id: int):
    """
    Packs the callback data for a conversation into one string.
    The total length of the string including separators must be under 64 bytes!

    :param command: The command where this conversation starts
    :param step: The step in the conversation.
    :param chat_id:
    :param message_id:
    :return:
    """
    callback_data_packed = f"{command};{step};{chat_id};{message_id}"
    if len(callback_data_packed.encode("utf-8")) > 64:
        print("callback_data cannot be formed! Args are too long!")
        return ""

    return callback_data_packed


def unpack_callback_data(callback_data: str):
    unpacked_dict = callback_data.split(";")
    command, step, chat_id, message_id = [i for i in unpacked_dict]

    data = CALLBACK_DATA[command][step]
    data["chat_id"] = chat_id
    data["message_id"] = message_id

    return data
