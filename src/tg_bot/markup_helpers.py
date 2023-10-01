"""
File        : markup_helpers.py
Author      : Diren D Bharwani
Date        : 2023-09-28

Description : Helper methods for dealing with callback data
"""
from typing import List

import telebot

from .conversation_state import ConversationState
from .callback_helpers import pack_callback_data


# ========================================================================================


def generate_button_definition(
    button_names: List[str],
    command: str,
    chat_id: int,
    conversation_state: ConversationState,
    back_button: bool = False,
):
    """
    Creates button definitions based on the conversation state. At least one next state must be defined!

    :param button_names: A list of strings for the names of each button. This must match the number of next_states!
    :param command: The command this button originates from
    :param chat_id: The chat_id where this conversation is happening
    :param conversation_state: The state of the conversation
    :param back_button: If a back button is created. The prev state must be defined for this!
    :return: The markup definition for a button as a dictionary
    """

    assert len(conversation_state.next_states) > 0
    assert len(button_names) == len(conversation_state.next_states)

    button_definitions = {}
    for i in range(0, len(button_names)):
        button_definitions[button_names[i]] = {
            "callback_data": pack_callback_data(
                command, chat_id, conversation_state.next_states[i]
            )
        }

    if back_button:
        assert conversation_state.prev_state is not None
        button_definitions["Back"] = {
            "callback_data": pack_callback_data(
                command, chat_id, conversation_state.prev_state
            )
        }

    return button_definitions


def generate_markup(button_definitions, row_width):
    markup = telebot.util.quick_markup(
        button_definitions,
        row_width,
    )

    return markup
