"""
File        : collections.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of helper variables and functions to clean up the interface between the entry point and
the rest of the project.
"""

from .start import command_start
from .credits import command_credits, callback_query_credits, Steps

# ======================================================================================================================

COMMAND_LIST = ["start", "credits"]

COMMAND_DICT = {"start": command_start, "credits": command_credits}

CALLBACK_QUERY_DICT = {"credits": callback_query_credits}

# Always follow this order:
# command: {
#   step: {
#       data...
#   }
# }
CALLBACK_DATA_DICT = {
    "credits": {
        Steps.BUY_CREDITS.value: {
            "command": "credits",
            "step": Steps.BUY_CREDITS.value,
        },
        Steps.PAY_PRORATE.value: {
            "command": "credits",
            "step": Steps.PAY_PRORATE.value,
        },
        Steps.PAY_PACKAGE.value: {
            "command": "credits",
            "step": Steps.PAY_PACKAGE.value,
        },
    }
}
