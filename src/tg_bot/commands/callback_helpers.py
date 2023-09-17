"""
File        : callback_helpers.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of methods to maintain a common standard for callback queries and callback data
"""

# ======================================================================================================================


def create_callback_data(command: str, step: str, chat_id: int):
    """
    Creates the string to be used as the callback data for InlineKeyboardButtons.
    The final string cannot exceed 64-bytes!

    :param command: The command where this callback_data falls under
    :param step: The step in the process of the conversation. Helps maintain a state.
    :param chat_id: The chat_id this data is tied to.
    :return: The string where each field is seperated by ;
    """

    final_string = f"{command};{step};{chat_id}"
    if len(final_string).encode("utf-8") > 64:
        raise ValueError(f"Incoming string from {command}: {step} is too long! Unable to create callback data!")

    return final_string
