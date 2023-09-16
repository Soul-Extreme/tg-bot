"""
File        : collections.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of helper variables and functions to clean up the interface between the entry point and
the rest of the project.
"""

from .start import command_start
from .credits import command_credits, callback_query_credits

# ======================================================================================================================

COMMAND_LIST = ["start", "credits"]

COMMAND_DICT = {"start": command_start, "credits": command_credits}

CALLBACK_QUERY_DICT = {"credits": callback_query_credits}
