from fastapi.testclient import TestClient

from main import app


VALID_HEADERS = {"X-Dashboard-Password": "change-me"}


def test_appointments_api_returns_expected_schema():
    client = TestClient(app)

    response = client.get("/api/appointments", headers=VALID_HEADERS)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["status"] == "Confirme"
    assert "email" in payload[0]
    assert "calendar_event_id" in payload[0]


def test_appointment_status_rejects_unknown_status():
    client = TestClient(app)

    response = client.patch(
        "/api/appointments/appt-1/status",
        headers=VALID_HEADERS,
        json={"status": "Inconnu"},
    )

    assert response.status_code == 422
