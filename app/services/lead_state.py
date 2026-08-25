from dataclasses import dataclass


@dataclass
class LeadState:
    full_name: str | None = None
    email: str | None = None
    contact_number: str | None = None
    company_name: str | None = None
    project_summary: str | None = None
    service_interest: str | None = None
    timeline: str | None = None
    budget_range: str | None = None

    def update_field(self, field_name: str, value: str) -> None:
        if not hasattr(self, field_name):
            raise ValueError(f"Unknown lead field: {field_name}")

        setattr(self, field_name, value)

    def next_required_field(self) -> str | None:
        if not self.full_name:
            return "full_name"

        if not self.email:
            return "email"

        if not self.contact_number:
            return "contact_number"

        return None

    def is_complete(self) -> bool:
        return self.next_required_field() is None