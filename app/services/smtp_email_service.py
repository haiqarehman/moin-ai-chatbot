import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.services.email_service import EmailService


class SMTPEmailService(EmailService):
    def send(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> bool:
        message = EmailMessage()

        message["From"] = settings.smtp_username
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        try:
            if settings.smtp_port == 465:
                with smtplib.SMTP_SSL(
                    settings.smtp_host,
                    settings.smtp_port,
                    timeout=15,
                ) as smtp:
                    smtp.login(
                        settings.smtp_username,
                        settings.smtp_password,
                    )
                    smtp.send_message(message)

            else:
                with smtplib.SMTP(
                    settings.smtp_host,
                    settings.smtp_port,
                    timeout=15,
                ) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login(
                        settings.smtp_username,
                        settings.smtp_password,
                    )
                    smtp.send_message(message)

            return True

        except Exception as exc:
            print(f"EMAIL SEND ERROR: {exc}")
            return False