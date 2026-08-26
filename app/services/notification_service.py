from app.services.delivery_status import DeliveryStatus
from app.services.email_service import EmailService
from app.services.lead_notification import build_lead_notification
from app.services.lead_state import LeadState


class NotificationService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
        self.last_delivery_status: DeliveryStatus | None = None

    def notify_lead(self, lead: LeadState) -> bool:
        notification = build_lead_notification(lead)

        success = self.email_service.send(
            recipient=notification["recipient"],
            subject=notification["subject"],
            body=notification["body"],
        )

        if success:
            self.last_delivery_status = DeliveryStatus.sent()
        else:
            self.last_delivery_status = DeliveryStatus.failed()

        return success