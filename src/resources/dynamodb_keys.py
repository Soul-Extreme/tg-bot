"""
File        : dynamodb_keys.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Defines a generic key set for associating it with a dynamoDB table.
"""

# ======================================================================================================================


class DynamoDBKey:
    """
    Defines a key for a DynamoDB table
    """

    def __init__(self, key_name: str, key_type: str):
        self.name = key_name
        self.type = key_type


class DynamoDBKeySet:
    """
    Defines a key set for an AWS DynamoDB table.
    """

    def __init__(
        self, partition_key: DynamoDBKey, sort_key: DynamoDBKey = None
    ):
        self.partition_key = partition_key
        self.sort_key = sort_key
