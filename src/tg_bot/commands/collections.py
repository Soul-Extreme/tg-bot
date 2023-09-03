"""
File        : collections.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of helper variables and functions to clean up the interface between the entry point and
the rest of the project.
"""

from .start import command_start, callback_query_start

# ======================================================================================================================

COMMAND_LIST = ["start"]

COMMAND_DICT = {"start": command_start}

CALLBACK_QUERY_DICT = {"start": callback_query_start}
