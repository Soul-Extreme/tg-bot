"""
File        : table_names.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Defines a set of variables with the table names and associated key sets.
"""

from enum import Enum

from .dynamodb_keyset import DynamoDBKeySet


# ======================================================================================================================

# ----------------------------------------
# Table Names
# ----------------------------------------


class Tables(Enum):
    PERSONAL_PARTICULARS = ("personal-particulars",)
    MEMBER_PROFILE = "member-profile"


# ----------------------------------------
# Table Keys
# ----------------------------------------

TABLE_KEYS = {
    Tables.PERSONAL_PARTICULARS: DynamoDBKeySet("chat_id"),
    Tables.MEMBER_PROFILE: DynamoDBKeySet("chat_id"),
}
