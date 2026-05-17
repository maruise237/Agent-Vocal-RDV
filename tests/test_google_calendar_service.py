from services.google_calendar_service import GoogleCalendarService


class FakeInsertRequest:
    def __init__(self, response):
        self.response = response

    def execute(self):
        return self.response


class FakeEventsResource:
    def __init__(self):
        self.insert_payload = None
        self.delete_payload = None

    def insert(self, calendarId, body, sendUpdates):
        self.insert_payload = {
            "calendarId": calendarId,
            "body": body,
            "sendUpdates": sendUpdates,
        }
        return FakeInsertRequest({"id": "evt-123", "htmlLink": "https://calendar/event"})

    def delete(self, calendarId, eventId, sendUpdates):
        self.delete_payload = {
            "calendarId": calendarId,
            "eventId": eventId,
            "sendUpdates": sendUpdates,
        }
        return FakeInsertRequest({})


class FakeGoogleService:
    def __init__(self):
        self.events_resource = FakeEventsResource()

    def events(self):
        return self.events_resource


def test_google_calendar_service_creates_event_payload():
    google_service = FakeGoogleService()
    calendar = GoogleCalendarService(
        google_service=google_service,
        calendar_id="primary",
        timezone="Africa/Douala",
        company_name="KamTech",
    )

    event_id = calendar.book_appointment(
        first_name="Nadia",
        last_name="Mbarga",
        email="nadia@example.com",
        date_rdv="2026-05-19 10:00",
        besoin="Audit agent vocal",
    )

    payload = google_service.events_resource.insert_payload
    assert event_id == "evt-123"
    assert payload["calendarId"] == "primary"
    assert payload["sendUpdates"] == "all"
    assert payload["body"]["summary"] == "RDV KamTech - Nadia Mbarga"
    assert payload["body"]["attendees"] == [{"email": "nadia@example.com"}]
    assert payload["body"]["start"]["dateTime"] == "2026-05-19T10:00:00"
    assert payload["body"]["end"]["dateTime"] == "2026-05-19T11:00:00"


def test_google_calendar_service_deletes_event():
    google_service = FakeGoogleService()
    calendar = GoogleCalendarService(
        google_service=google_service,
        calendar_id="primary",
        timezone="Africa/Douala",
        company_name="KamTech",
    )

    calendar.cancel_event("evt-123")

    payload = google_service.events_resource.delete_payload
    assert payload == {
        "calendarId": "primary",
        "eventId": "evt-123",
        "sendUpdates": "all",
    }
