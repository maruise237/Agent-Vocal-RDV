from fastapi.testclient import TestClient

from main import app


VALID_HEADERS = {"X-Dashboard-Password": "change-me"}


def test_availability_api_returns_default_windows():
    client = TestClient(app)

    response = client.get("/api/availability", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()[0]["label"] == "Semaine"


def test_availability_api_rejects_invalid_hours():
    client = TestClient(app)

    response = client.post(
        "/api/availability",
        headers=VALID_HEADERS,
        json=[{"id": "bad", "label": "Bad", "jours": [1], "debut": 18, "fin": 9}],
    )

    assert response.status_code == 422
