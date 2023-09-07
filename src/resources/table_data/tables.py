"""
File        : tables.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Defines a set of variables with the table names and associated key sets.
"""

from enum import Enum

import boto3.dynamodb.types

from src.resources.dynamodb_keys                          import DynamoDBKey, DynamoDBKeySet
from src.resources.table_data.personal_particulars_table    import PersonalParticularsFields
from src.resources.table_data.member_profile_table          import MemberProfileFields


# ======================================================================================================================


class Tables(Enum):
    PERSONAL_PARTICULARS    = "personal-particulars"
    MEMBER_PROFILE          = "member-profile"


TABLE_KEYS = {
    Tables.PERSONAL_PARTICULARS: DynamoDBKeySet(
        DynamoDBKey(PersonalParticularsFields.CHAT_ID.value, boto3.dynamodb.types.NUMBER)
    ),
    Tables.MEMBER_PROFILE: DynamoDBKeySet(
        DynamoDBKey(MemberProfileFields.CHAT_ID.value, boto3.dynamodb.types.NUMBER)
    ),
}
