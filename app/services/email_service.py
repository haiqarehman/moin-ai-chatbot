from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> bool:
        """Send an email and return whether delivery was accepted."""
        raise NotImplementedError