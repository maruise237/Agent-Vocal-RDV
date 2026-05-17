import httpx

from services.airtable_client import AirtableClient


def test_airtable_client_lists_records_with_bearer_token():
    captured_request = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_request
        captured_request = request
        return httpx.Response(200, json={"records": [{"id": "rec1", "fields": {"Nom": "Durand"}}]})

    client = AirtableClient(
        api_key="pat-test",
        base_id="app-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    records = client.list_records("Rendez-vous")

    assert records == [{"id": "rec1", "fields": {"Nom": "Durand"}}]
    assert captured_request is not None
    assert captured_request.url.path == "/v0/app-test/Rendez-vous"
    assert captured_request.headers["authorization"] == "Bearer pat-test"


def test_airtable_client_creates_record_with_fields_payload():
    captured_json = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_json
        captured_json = request.read().decode()
        return httpx.Response(200, json={"id": "rec-created", "fields": {"Nom": "Durand"}})

    client = AirtableClient(
        api_key="pat-test",
        base_id="app-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    record = client.create_record("Rendez-vous", {"Nom": "Durand"})

    assert record["id"] == "rec-created"
    assert '"fields":{"Nom":"Durand"}' in captured_json


def test_airtable_client_updates_record_with_patch():
    captured_method = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_method
        captured_method = request.method
        return httpx.Response(200, json={"id": "rec1", "fields": {"Statut": "Annule"}})

    client = AirtableClient(
        api_key="pat-test",
        base_id="app-test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    record = client.update_record("Rendez-vous", "rec1", {"Statut": "Annule"})

    assert captured_method == "PATCH"
    assert record["fields"]["Statut"] == "Annule"
