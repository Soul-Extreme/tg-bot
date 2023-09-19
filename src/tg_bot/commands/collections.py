"""
File        : collections.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of helper variables and functions to clean up the interface between the entry point and
the rest of the project.
"""

from enum import Enum
from .start import command_start
from .credits import command_credits, callback_query_credits

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


COMMAND_MAP = {"start": command_start, "credits": command_credits}

CALLBACK_QUERY_MAP = {"credits": callback_query_credits}

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
    }
}

CLASS_PRICING = {"Student": {"Individual": 10, "Package": 25}, "Alumni": {"Individual": 13, "Package": 35}}
