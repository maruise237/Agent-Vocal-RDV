from fastapi.testclient import TestClient

from main import app


def test_availability_editor_exposes_smart_controls():
    client = TestClient(app)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "availability-preset" in response.text
    assert "day-toggle" in response.text
    assert "add-availability" in response.text
    assert "buildHourOptions" in response.text
    assert "validateAvailabilityDraft" in response.text
