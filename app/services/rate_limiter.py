import time


class RateLimiter:
    def __init__(
        self,
        max_requests: int = 5,
        window_seconds: int = 60,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    def allow(self, client_id: str) -> bool:
        now = time.time()

        timestamps = self._requests.setdefault(
            client_id,
            [],
        )

        timestamps[:] = [
            timestamp
            for timestamp in timestamps
            if now - timestamp < self.window_seconds
        ]

        if len(timestamps) >= self.max_requests:
            return False

        timestamps.append(now)

        return True