"""
File        : command_function_maps.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of maps to map commands and callback queries to their command texts.
"""

from src.tg_bot.commands.register import command_register
from src.tg_bot.commands.credits import (
    command_credits,
    command_successful_payment,
    callback_query_credits,
)

# ======================================================================================================================

COMMAND_LIST = ["register", "credits", "successful_payment"]

COMMAND_MAP = {
    "register": command_register,
    "credits": command_credits,
    "successful_payment": command_successful_payment,
}

CALLBACK_QUERY_MAP = {"credits": callback_query_credits}
