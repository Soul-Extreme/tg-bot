import json


def handler(event, context):
    body = {
        "message": "Hello tg-bot!",
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}
