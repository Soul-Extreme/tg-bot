"""
File        : callback_helpers.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : Helper methods for dealing with callback data
"""

from enum import Enum

# ======================================================================================================================


class Step(Enum):
    def __str__(self):
        return self.value


class CreditsStep(str, Step):
    BUY_CREDITS = "buy_credits"
    PAY_INDIVIDUAL = "pay_individual"
    PAY_PACKAGE = "pay_package"
    INDIVIDUAL_X1 = "individual_x1"
    INDIVIDUAL_X2 = "individual_x2"


CALLBACK_DATA = {
    "credits": {
        CreditsStep.BUY_CREDITS.value: {
            "command": "credits",
            "step": CreditsStep.BUY_CREDITS.value,
        },
        CreditsStep.PAY_INDIVIDUAL.value: {
            "command": "credits",
            "step": CreditsStep.PAY_INDIVIDUAL.value,
        },
        CreditsStep.PAY_PACKAGE.value: {
            "command": "credits",
            "step": CreditsStep.PAY_PACKAGE.value,
        },
        CreditsStep.INDIVIDUAL_X1.value: {
            "command": "credits",
            "step": CreditsStep.INDIVIDUAL_X1.value
        },
        CreditsStep.INDIVIDUAL_X2.value: {
            "command": "credits",
            "step": CreditsStep.INDIVIDUAL_X2.value
        }
    }
}


def pack_callback_data(command: str, step: Step, chat_id: int):
    """
    Packs the callback data for a conversation into one string.
    The total length of the string including separators must be under 64 bytes!

    :param command: The command where this conversation starts
    :param step: The step in the conversation.
    :param chat_id:
    :return:
    """
    callback_data_packed = f"{command};{step};{chat_id}"
    if len(callback_data_packed.encode("utf-8")) > 64:
        print("callback_data cannot be formed! Args are too long!")
        return ""

    return callback_data_packed


def unpack_callback_data(callback_data: str):
    unpacked_dict = callback_data.split(";")
    command, step, chat_id = [i for i in unpacked_dict]

    data = CALLBACK_DATA[command][step]
    data["chat_id"] = chat_id

    return data
