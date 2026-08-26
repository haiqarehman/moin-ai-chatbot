from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class DeliveryStatus:
    status: str
    timestamp: datetime

    @classmethod
    def sent(cls) -> "DeliveryStatus":
        return cls(
            status="sent",
            timestamp=datetime.now(timezone.utc),
        )

    @classmethod
    def failed(cls) -> "DeliveryStatus":
        return cls(
            status="failed",
            timestamp=datetime.now(timezone.utc),
        )