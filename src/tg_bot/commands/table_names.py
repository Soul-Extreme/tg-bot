"""
File        : table_names.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Defines a set of variables with the table names and associated key sets.
"""

from enum import Enum

from .dynamodb_keyset import KeySet


# ======================================================================================================================

# ----------------------------------------
# Table Names
# ----------------------------------------

class Tables(Enum):
    PERSONAL_PARTICULARS = "personal-particulars"


# ----------------------------------------
# Table Keys
# ----------------------------------------

TABLE_KEYS = {
    Tables.PERSONAL_PARTICULARS.value: KeySet("chat_id")
}
