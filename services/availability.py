from models import AvailabilityWindow
from services.airtable_client import AirtableClient
from services.airtable_repositories import AirtableAvailabilityRepository
from settings import get_settings


class AvailabilityService:
    def __init__(self) -> None:
        self._windows: list[AvailabilityWindow] = [
            AvailabilityWindow(
                id="week",
                label="Semaine",
                jours=[0, 1, 2, 3, 4],
                debut=9,
                fin=17,
            )
        ]

    def list_windows(self) -> list[AvailabilityWindow]:
        return self._windows

    def save_windows(
        self, windows: list[AvailabilityWindow]
    ) -> list[AvailabilityWindow]:
        self._windows = windows
        return self._windows


def build_availability_service():
    settings = get_settings()
    if settings.airtable_api_key and settings.airtable_base_id:
        return AirtableAvailabilityRepository(
            AirtableClient(settings.airtable_api_key, settings.airtable_base_id),
            settings.airtable_config_table,
        )
    return AvailabilityService()


availability_service = build_availability_service()
