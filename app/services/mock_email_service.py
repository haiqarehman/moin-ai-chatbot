from app.services.email_service import EmailService


class MockEmailService(EmailService):
    def __init__(
        self,
        should_succeed: bool = True,
        failures_before_success: int = 0,
    ):
        self.should_succeed = should_succeed
        self.failures_before_success = failures_before_success
        self.attempts = 0
        self.sent_emails: list[dict] = []

    def send(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> bool:
        self.attempts += 1

        if not self.should_succeed:
            return False

        if self.attempts <= self.failures_before_success:
            return False

        self.sent_emails.append(
            {
                "recipient": recipient,
                "subject": subject,
                "body": body,
            }
        )

        return True