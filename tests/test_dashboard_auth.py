from fastapi.testclient import TestClient

from main import app


def test_dashboard_page_renders_login_shell():
    client = TestClient(app)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Agent Vocal RDV" in response.text
    assert "dashboard-root" in response.text


def test_appointments_api_rejects_invalid_password():
    client = TestClient(app)

    response = client.get("/api/appointments", headers={"X-Dashboard-Password": "bad"})

    assert response.status_code == 401
