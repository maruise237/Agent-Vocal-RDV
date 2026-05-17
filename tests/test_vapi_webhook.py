from fastapi.testclient import TestClient

from main import app


def test_vapi_webhook_verifier_disponibilites_returns_tool_result():
    client = TestClient(app)

    response = client.post(
        "/webhook",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tc-slots",
                        "function": {
                            "name": "verifier_disponibilites",
                            "arguments": '{"jours": 7}',
                        },
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json()["results"][0]["toolCallId"] == "tc-slots"
    assert "Créneaux disponibles" in response.json()["results"][0]["result"]


def test_vapi_webhook_reserver_creneau_creates_appointment_result():
    client = TestClient(app)

    response = client.post(
        "/webhook",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tc-book",
                        "function": {
                            "name": "reserver_creneau",
                            "arguments": (
                                '{"prenom":"Nadia","nom":"Mbarga",'
                                '"email":"nadia@example.com",'
                                '"date_rdv":"2026-05-19 10:00",'
                                '"besoin":"Audit agent vocal","call_id":"call-123"}'
                            ),
                        },
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["toolCallId"] == "tc-book"
    assert "Rendez-vous confirmé" in result["result"]
    assert "Nadia Mbarga" in result["result"]


def test_vapi_webhook_unknown_tool_returns_readable_error():
    client = TestClient(app)

    response = client.post(
        "/webhook",
        json={
            "message": {
                "type": "tool-calls",
                "toolCallList": [
                    {
                        "id": "tc-unknown",
                        "function": {"name": "outil_inconnu", "arguments": "{}"},
                    }
                ],
            }
        },
    )

    assert response.status_code == 200
    assert response.json()["results"][0]["toolCallId"] == "tc-unknown"
    assert "Outil inconnu" in response.json()["results"][0]["result"]
