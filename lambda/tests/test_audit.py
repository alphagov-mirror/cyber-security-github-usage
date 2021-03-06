import json
import os

import pytest
import stubs

import audit


@pytest.mark.usefixtures("event_body")
def test_create_sns_message(event_body):
    """ Create the message to publish to SNS """
    audit_id = 0
    sns_message = audit.create_sns_message(audit_id, event_body)
    message = json.loads(sns_message)
    assert message["lambda"] == json.dumps(event_body)


@pytest.mark.usefixtures("event_body")
def test_publish_alert(event_body):
    """ Publish alert message to SNS """
    audit_id = 0
    sns_message = audit.create_sns_message(audit_id, event_body)
    topic_arn = "arn:aws:sns:eu-west-2:123456789012:my-topic"
    sns_subject = "GitHub organization access audit"
    sns_message_id = "test123"
    os.environ["SNS_ARN"] = topic_arn

    stubber = stubs.mock_sns_publish(
        sns_message, topic_arn, sns_subject, sns_message_id
    )

    with stubber:
        response = audit.publish_alert(audit_id, sns_message)
        assert response["MessageId"] == sns_message_id

        stubber.deactivate()


def test_make_audit_event():
    test_event = {"type": "Test", "org": "alphagov", "count": 12}

    event = audit.make_audit_event(type=test_event["type"])
    assert event["type"] == test_event["type"]
    # Check the org key is present but None
    assert event["org"] is None

    event = audit.make_audit_event(type=test_event["type"], org=test_event["org"])
    assert event["type"] == test_event["type"]
    assert event["org"] == test_event["org"]
    # Check the repository key is present but None
    assert event["repository"] is None

    event = audit.make_audit_event(
        type=test_event["type"], org=test_event["org"], count=test_event["count"]
    )
    assert event["count"] == 12
    assert event["member"] is None
