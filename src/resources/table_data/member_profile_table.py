"""
File        : member_profile.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description :
    Defines variables pertaining to the personal-particulars dynamoDB table.
    This file serves as a single source of truth for all variables relating to this table.
"""

from enum import Enum

# ======================================================================================================================


class MemberProfileFields(Enum):
    CHAT_ID = "chat_id"
    STUDENT_STATUS = "student_status"
    GENRE = "genre"
    CREDITS = "credits"
    ADMIN = "admin"
