from typing import Any
from urllib.parse import quote

import httpx
from fastapi import HTTPException, status


class AirtableClient:
    def __init__(
        self,
        api_key: str,
        base_id: str,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_id = base_id
        self.http_client = http_client or httpx.Client(timeout=20)

    def list_records(self, table_name: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        offset: str | None = None

        while True:
            params = {"pageSize": 100}
            if offset:
                params["offset"] = offset

            payload = self._request("GET", table_name, params=params)
            records.extend(payload.get("records", []))

            offset = payload.get("offset")
            if not offset:
                return records

    def create_record(
        self, table_name: str, fields: dict[str, Any]
    ) -> dict[str, Any]:
        return self._request("POST", table_name, json={"fields": fields})

    def update_record(
        self, table_name: str, record_id: str, fields: dict[str, Any]
    ) -> dict[str, Any]:
        return self._request("PATCH", table_name, record_id, json={"fields": fields})

    def _request(
        self,
        method: str,
        table_name: str,
        record_id: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        encoded_table = quote(table_name, safe="")
        url = f"https://api.airtable.com/v0/{self.base_id}/{encoded_table}"
        if record_id:
            url = f"{url}/{record_id}"

        response = self.http_client.request(
            method,
            url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            **kwargs,
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "Airtable est inaccessible ou mal configuré. "
                    "Vérifie AIRTABLE_API_KEY, AIRTABLE_BASE_ID et les noms de tables."
                ),
            ) from exc
        return response.json()
