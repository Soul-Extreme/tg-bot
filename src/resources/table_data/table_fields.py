"""
File        : table_fields.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description :
Defines enums for accessing fields of the dynamoDB tables.
This file serves as a single source of truth for all variables relating to tables.
Custom fields should be handled specifically within those files/functions.
"""

from enum import Enum

# ======================================================================================================================


class PersonalParticularsFields(str, Enum):
    CHAT_ID = "chat_id"
    FULL_NAME = "full_name"
    PREFERRED_NAME = "preferred_name"
    PHONE_NUMBER = "phone_number"
    TELEGRAM_HANDLE = "telegram_handle"
    NRIC_LAST4 = "nric_last4"
    STUDENT_STATUS = "student_status"
    STUDENT_ID = "student_id"
    CLUSTER = "cluster"
    PROGRAMME = "programme"
    YEAR = "year"
    GRADUATION_YEAR = "graduation_year"
    EMERGENCY_CONTACT_NAME = "emergency_contact_name"
    EMERGENCY_CONTACT_RELATION = "emergency_contact_relation"
    EMERGENCY_CONTACT_NUMBER = "emergency_contact_relation"
    GENRE = "genre"
    SHIRT_SIZE = "shirt_size"
    JACKET_SIZE = "jacket_size"


class MemberProfileFields(str, Enum):
    CHAT_ID = "chat_id"
    STUDENT_STATUS = "student_status"
    GENRE = "genre"
    CREDITS = "credits"
    ADMIN = "admin"


class ChatStateFields(str, Enum):
    COMMAND = "command"
    CHAT_ID = "chat_id"
    TTL = "Time To Live"
