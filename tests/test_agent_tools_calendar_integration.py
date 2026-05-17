from services import agent_tools
from settings import get_settings


class FakeCalendar:
    def book_appointment(self, **kwargs):
        return "evt-fake-123"


def test_reserver_creneau_attaches_calendar_event_when_configured(monkeypatch):
    settings = get_settings()
    settings.google_service_account_json = '{"type":"service_account"}'
    settings.google_calendar_id = "primary"
    settings.google_calendar_timezone = "Africa/Douala"
    settings.company_name = "KamTech"

    monkeypatch.setattr(
        agent_tools,
        "build_configured_google_calendar_service",
        lambda: FakeCalendar(),
    )

    result = agent_tools.reserver_creneau(
        prenom="Nadia",
        nom="Mbarga",
        email="nadia@example.com",
        date_rdv="2026-05-19 10:00",
        besoin="Audit agent vocal",
        call_id="call-calendar",
    )

    created = agent_tools.appointment_service.list_appointments()[-1]
    assert "Rendez-vous confirmé" in result
    assert created.calendar_event_id == "evt-fake-123"

    settings.google_service_account_json = None
