from datetime import datetime, timezone

from app.services.delivery_status import DeliveryStatus


def test_sent_delivery_status_contains_timestamp():
    status = DeliveryStatus.sent()

    assert status.status == "sent"
    assert isinstance(status.timestamp, datetime)
    assert status.timestamp.tzinfo == timezone.utc


def test_failed_delivery_status_contains_timestamp():
    status = DeliveryStatus.failed()

    assert status.status == "failed"
    assert isinstance(status.timestamp, datetime)
    assert status.timestamp.tzinfo == timezone.utc