from fastapi.testclient import TestClient

from main import app


def test_health_route_returns_active_status():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "Agent Vocal RDV actif"}
