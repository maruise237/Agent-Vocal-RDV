import httpx
import pytest
from fastapi import HTTPException

from services.airtable_client import AirtableClient
from services.airtable_repositories import AirtableAppointmentRepository


def test_airtable_repository_returns_clear_http_error_on_forbidden():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"error": {"message": "Forbidden"}})

    repository = AirtableAppointmentRepository(
        AirtableClient(
            api_key="pat-test",
            base_id="app-wrong",
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
        "Rendez-vous",
    )

    with pytest.raises(HTTPException) as exc_info:
        repository.list_appointments()

    assert exc_info.value.status_code == 502
    assert "Airtable" in exc_info.value.detail
