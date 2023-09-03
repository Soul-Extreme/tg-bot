"""
File        : collections.py
Author      : Diren D Bharwani
Date        : 2023-08-30

Description : A collection of helper variables and functions to clean up the interface between the entry point and
the rest of the project.
"""

import start

# ======================================================================================================================

COMMAND_LIST = ["start"]

COMMAND_DICT = {"start": start.command}

CALLBACK_QUERY_DICT = {"start": start.handle_callback_query}
