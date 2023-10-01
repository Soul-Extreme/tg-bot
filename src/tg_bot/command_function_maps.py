"""
File        : command_function_maps.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of maps to map commands and callback queries to their command texts.
"""

from src.tg_bot.commands.register import command_register
from src.tg_bot.commands.credits import command_credits, callback_query_credits

# ======================================================================================================================

COMMAND_LIST = ["register", "credits"]

COMMAND_MAP = {"register": command_register, "credits": command_credits}

CALLBACK_QUERY_MAP = {"credits": callback_query_credits}
