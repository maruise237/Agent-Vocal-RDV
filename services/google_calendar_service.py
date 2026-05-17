import json
from datetime import datetime, timedelta
from typing import Any, Protocol
from urllib.parse import quote

import httpx


class GoogleEventsResource(Protocol):
    def insert(self, calendarId: str, body: dict[str, Any], sendUpdates: str):
        ...

    def delete(self, calendarId: str, eventId: str, sendUpdates: str):
        ...


class GoogleCalendarApi(Protocol):
    def events(self) -> GoogleEventsResource:
        ...


class GoogleCalendarService:
    def __init__(
        self,
        google_service: GoogleCalendarApi,
        calendar_id: str,
        timezone: str,
        company_name: str,
        appointment_duration_minutes: int = 60,
    ) -> None:
        self.google_service = google_service
        self.calendar_id = calendar_id
        self.timezone = timezone
        self.company_name = company_name
        self.appointment_duration_minutes = appointment_duration_minutes

    def book_appointment(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_rdv: str,
        besoin: str,
    ) -> str:
        start_at = datetime.strptime(date_rdv, "%Y-%m-%d %H:%M")
        end_at = start_at + timedelta(minutes=self.appointment_duration_minutes)
        event = {
            "summary": f"RDV {self.company_name} - {first_name} {last_name}",
            "description": f"Besoin client : {besoin}",
            "start": {
                "dateTime": start_at.isoformat(),
                "timeZone": self.timezone,
            },
            "end": {
                "dateTime": end_at.isoformat(),
                "timeZone": self.timezone,
            },
            "attendees": [{"email": email}],
        }

        created_event = (
            self.google_service.events()
            .insert(calendarId=self.calendar_id, body=event, sendUpdates="all")
            .execute()
        )
        return created_event["id"]

    def cancel_event(self, event_id: str) -> None:
        (
            self.google_service.events()
            .delete(calendarId=self.calendar_id, eventId=event_id, sendUpdates="all")
            .execute()
        )


class GoogleCalendarRestRequest:
    def __init__(self, response: httpx.Response) -> None:
        self.response = response

    def execute(self) -> dict[str, Any]:
        self.response.raise_for_status()
        if not self.response.content:
            return {}
        return self.response.json()


class GoogleCalendarRestEvents:
    def __init__(self, credentials: Any, http_client: httpx.Client | None = None) -> None:
        self.credentials = credentials
        self.http_client = http_client or httpx.Client(timeout=20)

    def insert(self, calendarId: str, body: dict[str, Any], sendUpdates: str):
        calendar_id = quote(calendarId, safe="")
        response = self.http_client.post(
            f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events",
            params={"sendUpdates": sendUpdates},
            headers=self._headers(),
            json=body,
        )
        return GoogleCalendarRestRequest(response)

    def delete(self, calendarId: str, eventId: str, sendUpdates: str):
        calendar_id = quote(calendarId, safe="")
        event_id = quote(eventId, safe="")
        response = self.http_client.delete(
            f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}",
            params={"sendUpdates": sendUpdates},
            headers=self._headers(),
        )
        return GoogleCalendarRestRequest(response)

    def _headers(self) -> dict[str, str]:
        from google.auth.transport.requests import Request

        if not self.credentials.valid:
            self.credentials.refresh(Request())
        return {"Authorization": f"Bearer {self.credentials.token}"}


class GoogleCalendarRestApi:
    def __init__(self, credentials: Any) -> None:
        self.events_resource = GoogleCalendarRestEvents(credentials)

    def events(self) -> GoogleCalendarRestEvents:
        return self.events_resource


def build_google_calendar_service(
    service_account_json: str,
    calendar_id: str,
    timezone: str,
    company_name: str,
) -> GoogleCalendarService:
    from google.oauth2 import service_account

    credentials_info = json.loads(service_account_json)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/calendar"],
    )
    google_service = GoogleCalendarRestApi(credentials)
    return GoogleCalendarService(
        google_service=google_service,
        calendar_id=calendar_id,
        timezone=timezone,
        company_name=company_name,
    )


def build_configured_google_calendar_service() -> GoogleCalendarService | None:
    from settings import get_settings

    settings = get_settings()
    if not settings.google_service_account_json:
        return None

    return build_google_calendar_service(
        service_account_json=settings.google_service_account_json,
        calendar_id=settings.google_calendar_id,
        timezone=settings.google_calendar_timezone,
        company_name=settings.company_name,
    )
