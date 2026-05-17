import httpx

from setup_vapi import VapiClient, build_assistant_payload


def test_build_assistant_payload_contains_webhook_and_tools():
    payload = build_assistant_payload(
        company_name="KamTech",
        company_description="Agence IA locale",
        first_message="Bonjour, comment puis-je vous aider ?",
        webhook_url="https://agent.example.com/webhook",
        voice_id="voice-123",
    )

    tools = payload["model"]["tools"]
    tool_names = [tool["function"]["name"] for tool in tools]

    assert payload["serverUrl"] == "https://agent.example.com/webhook"
    assert payload["voice"]["voiceId"] == "voice-123"
    assert "verifier_disponibilites" in tool_names
    assert "reserver_creneau" in tool_names
    assert "KamTech" in payload["model"]["messages"][0]["content"]


def test_vapi_client_creates_assistant_with_private_key():
    captured_request = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_request
        captured_request = request
        return httpx.Response(201, json={"id": "assistant-123"})

    client = VapiClient(
        private_key="vapi-private",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    response = client.create_assistant({"name": "Agent RDV"})

    assert response["id"] == "assistant-123"
    assert captured_request is not None
    assert captured_request.url.path == "/assistant"
    assert captured_request.headers["authorization"] == "Bearer vapi-private"
