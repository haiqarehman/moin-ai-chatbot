from app.services.lead_state import LeadState
from app.services.lead_validator import validate_email


class LeadCaptureService:
    def capture(
        self,
        lead: LeadState,
        field_name: str,
        value: str,
    ) -> str | None:

        value = value.strip()

        if field_name == "email" and not validate_email(value):
            raise ValueError("Invalid email address.")

        lead.update_field(field_name, value)

        return lead.next_required_field()