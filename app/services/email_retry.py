from app.services.email_service import EmailService


class RetryingEmailService(EmailService):
    def __init__(
        self,
        email_service: EmailService,
        max_attempts: int = 3,
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self.email_service = email_service
        self.max_attempts = max_attempts
        self.attempts = 0

    def send(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> bool:
        self.attempts = 0

        for _ in range(self.max_attempts):
            self.attempts += 1

            if self.email_service.send(
                recipient,
                subject,
                body,
            ):
                return True

        return False