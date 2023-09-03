"""
File        : dynamodb_keyset.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Defines a generic key set for associating it with a dynamoDB table.
"""

import string


# ======================================================================================================================

class DynamoDBKeySet:
    """
    Defines a key set for an AWS DynamoDB table.
    """

    def __init__(self, partition_key: string, sort_key: string = None):
        self.partition_key = partition_key
        self.sort_key = sort_key
