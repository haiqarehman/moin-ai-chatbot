from app.services.lead_state import LeadState


NOTIFICATION_RECIPIENT = "info@moinsystemsai.com"


def build_lead_notification(lead: LeadState) -> dict:
    subject = "New Lead Captured"

    body = f"""
New lead captured from MoinSystems AI chatbot.

Name: {lead.full_name or "Not provided"}
Email: {lead.email or "Not provided"}
Contact Number: {lead.contact_number or "Not provided"}

Company: {lead.company_name or "Not provided"}
Project Summary: {lead.project_summary or "Not provided"}
Service Interest: {lead.service_interest or "Not provided"}
Timeline: {lead.timeline or "Not provided"}
Budget Range: {lead.budget_range or "Not provided"}
""".strip()

    return {
        "recipient": NOTIFICATION_RECIPIENT,
        "subject": subject,
        "body": body,
    }