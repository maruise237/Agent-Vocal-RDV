from fastapi.testclient import TestClient

import dashboard
from main import app


class FakeCalendar:
    def __init__(self):
        self.cancelled_event_id = None

    def cancel_event(self, event_id):
        self.cancelled_event_id = event_id


def test_dashboard_cancels_calendar_event_when_appointment_is_cancelled(monkeypatch):
    fake_calendar = FakeCalendar()
    monkeypatch.setattr(
        dashboard,
        "build_configured_google_calendar_service",
        lambda: fake_calendar,
    )

    client = TestClient(app)
    response = client.patch(
        "/api/appointments/appt-1/status",
        headers={"X-Dashboard-Password": "change-me"},
        json={"status": "Annule"},
    )

    assert response.status_code == 200
    assert fake_calendar.cancelled_event_id == "calendar-demo-1"
