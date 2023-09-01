"""
File        : command_list.py
Author      : Diren D Bharwani
Date        : 2023-09-01

Description : Defines the list of commands used by the bot and a map for strings to the functions
"""

from .start import start_command

# ======================================================================================================================

command_list = [
    'start'
]

command_dict = {
    'start': start_command
}
