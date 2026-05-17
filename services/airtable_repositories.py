import json
from datetime import datetime
from typing import Protocol

from models import Appointment, AppointmentStatus, AvailabilityWindow


AVAILABILITY_CONFIG_KEY = "availability_windows"


class AirtableLikeClient(Protocol):
    def list_records(self, table_name: str) -> list[dict]:
        ...

    def create_record(self, table_name: str, fields: dict) -> dict:
        ...

    def update_record(self, table_name: str, record_id: str, fields: dict) -> dict:
        ...


class AirtableAppointmentRepository:
    def __init__(self, client: AirtableLikeClient, table_name: str) -> None:
        self.client = client
        self.table_name = table_name

    def list_appointments(self) -> list[Appointment]:
        return [
            self._record_to_appointment(record)
            for record in self.client.list_records(self.table_name)
        ]

    def create_appointment(
        self,
        first_name: str,
        last_name: str,
        email: str,
        date_rdv: str,
        besoin: str,
        call_id: str | None = None,
        calendar_event_id: str | None = None,
    ) -> Appointment:
        fields = {
            "Prenom": first_name,
            "Nom": last_name,
            "Email": email,
            "Date RDV": date_rdv,
            "Besoin": besoin,
            "Statut": AppointmentStatus.CONFIRME.value,
            "Cree le": datetime.utcnow().replace(microsecond=0).isoformat(),
        }
        if call_id:
            fields["Call ID"] = call_id
        if calendar_event_id:
            fields["Calendar Event ID"] = calendar_event_id

        record = self.client.create_record(self.table_name, fields)
        return self._record_to_appointment(record)

    def update_status(
        self, appointment_id: str, new_status: AppointmentStatus
    ) -> Appointment:
        record = self.client.update_record(
            self.table_name, appointment_id, {"Statut": new_status.value}
        )
        return self._record_to_appointment(record)

    def _record_to_appointment(self, record: dict) -> Appointment:
        fields = record.get("fields", {})
        return Appointment(
            id=record["id"],
            first_name=fields.get("Prenom", ""),
            last_name=fields.get("Nom", ""),
            email=fields.get("Email", "unknown@example.com"),
            date_rdv=fields.get("Date RDV", ""),
            besoin=fields.get("Besoin", ""),
            status=AppointmentStatus(fields.get("Statut", AppointmentStatus.CONFIRME.value)),
            created_at=fields.get("Cree le", ""),
            call_id=fields.get("Call ID"),
            calendar_event_id=fields.get("Calendar Event ID"),
        )


class AirtableAvailabilityRepository:
    def __init__(self, client: AirtableLikeClient, table_name: str) -> None:
        self.client = client
        self.table_name = table_name

    def list_windows(self) -> list[AvailabilityWindow]:
        config_record = self._find_config_record()
        if config_record is None:
            return []

        raw_value = config_record.get("fields", {}).get("Valeur", "[]")
        return [AvailabilityWindow(**item) for item in json.loads(raw_value)]

    def save_windows(
        self, windows: list[AvailabilityWindow]
    ) -> list[AvailabilityWindow]:
        fields = {
            "Cle": AVAILABILITY_CONFIG_KEY,
            "Valeur": json.dumps(
                [window.model_dump() for window in windows],
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        }

        config_record = self._find_config_record()
        if config_record is None:
            self.client.create_record(self.table_name, fields)
        else:
            self.client.update_record(self.table_name, config_record["id"], fields)

        return windows

    def _find_config_record(self) -> dict | None:
        for record in self.client.list_records(self.table_name):
            if record.get("fields", {}).get("Cle") == AVAILABILITY_CONFIG_KEY:
                return record
        return None
