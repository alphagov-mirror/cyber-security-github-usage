""" Parse messages from sns event """
import json


def get_message_body(message):
    """ Return json decoded message body from either SNS or SQS event model """
    print(str(message))
    try:
        message_text = message["body"]
        # catch addict default behaviour for missing keys
        if message_text == {}:
            raise KeyError

    except KeyError:
        message_text = message["Sns"]["Message"]

    try:
        message_body = json.loads(message_text)
    except (TypeError, json.JSONDecodeError):
        message_body = message_text

    print(str(message_body))
    return message_body


def parse_messages(event):
    """
    Parse the escaped message body from each of the SQS messages in event.Records
    """
    if "Records" in event:
        messages = [get_message_body(record) for record in event["Records"]]
    elif "body" in event:
        messages = [get_message_body(event)]
    else:
        default_message = { "action": "usage" }
        messages = [default_message]
    print(str(messages))
    return messages