"""
File        : dynamodb_table.py
Author      : Diren D Bharwani
Date        : 2023-09-03

Description : Defines a generic dynamoDB Table object
"""

import boto3
from botocore.exceptions import ClientError


# ======================================================================================================================

class DynamoDBTable:
    """
    Encapsulates an AWS DynamoDB Table
    """

    def __init__(self, table_name, keys):
        """
        Constructor for a DynamoDB Table

        :param table_name: The name of the dynamodb table
        :param keys: The keys used to access data in the table stored as a dictionary.
        """

        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.table(self.table_name)

        self.keys = keys

    def put_item(self, item):
        """
        Puts an item into the table.

        :param item: The item to put into the table.
        :return: True if the item was put in. False if it failed to put.
        """
        try:
            self.table.put_item(Item=item)
        except ClientError as error:
            print(f"Error putting item into {self.table_name}: {error}")
            return False

        return True

    def get_item(self, partition_key_value, sort_key_value=None):
        """
        Retrieves an item from the table.

        :param partition_key_value: The value of a partition key to access an item. There is always a partition key.

        :param sort_key_value: The value of sort key to access an item. This is an optional key and may be ignored if
        not required.

        :return: The retrieved item as a dict. An empty dict is return if nothing was found.
        """
        try:
            key = {
                self.keys.partition_key: partition_key_value
            }

            if sort_key_value is not None:
                key[self.keys.sort_key] = sort_key_value

            response = self.table.get_item(key)
            return response["Item"]

        except KeyError as error:
            print("Item could not be found!")
            return {}
