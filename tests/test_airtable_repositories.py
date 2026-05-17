from services.airtable_repositories import (
    AirtableAppointmentRepository,
    AirtableAvailabilityRepository,
)
from models import AppointmentStatus, AvailabilityWindow


class FakeAirtableClient:
    def __init__(self) -> None:
        self.created_fields = None
        self.updated_fields = None

    def list_records(self, table_name):
        if table_name == "Rendez-vous":
            return [
                {
                    "id": "rec-rdv",
                    "fields": {
                        "Prenom": "Nadia",
                        "Nom": "Mbarga",
                        "Email": "nadia@example.com",
                        "Date RDV": "2026-05-19 10:00",
                        "Besoin": "Audit agent vocal",
                        "Statut": "Confirme",
                        "Cree le": "2026-05-17T00:00:00",
                        "Call ID": "call-123",
                        "Calendar Event ID": "evt-123",
                    },
                }
            ]
        return [
            {
                "id": "rec-config",
                "fields": {
                    "Cle": "availability_windows",
                    "Valeur": '[{"id":"week","label":"Semaine","jours":[0,1,2,3,4],"debut":9,"fin":17}]',
                },
            }
        ]

    def create_record(self, table_name, fields):
        self.created_fields = fields
        return {"id": "rec-new", "fields": fields}

    def update_record(self, table_name, record_id, fields):
        self.updated_fields = fields
        return {"id": record_id, "fields": fields}


def test_airtable_appointment_repository_maps_records_to_model():
    repository = AirtableAppointmentRepository(FakeAirtableClient(), "Rendez-vous")

    appointments = repository.list_appointments()

    assert appointments[0].id == "rec-rdv"
    assert appointments[0].first_name == "Nadia"
    assert appointments[0].status == AppointmentStatus.CONFIRME


def test_airtable_appointment_repository_maps_create_payload():
    fake_client = FakeAirtableClient()
    repository = AirtableAppointmentRepository(fake_client, "Rendez-vous")

    appointment = repository.create_appointment(
        first_name="Nadia",
        last_name="Mbarga",
        email="nadia@example.com",
        date_rdv="2026-05-19 10:00",
        besoin="Audit agent vocal",
        call_id="call-123",
    )

    assert appointment.id == "rec-new"
    assert fake_client.created_fields["Prenom"] == "Nadia"
    assert fake_client.created_fields["Statut"] == "Confirme"


def test_airtable_availability_repository_loads_and_saves_config_json():
    fake_client = FakeAirtableClient()
    repository = AirtableAvailabilityRepository(fake_client, "Config")

    windows = repository.list_windows()
    saved = repository.save_windows(
        [AvailabilityWindow(id="weekend", label="Week-end", jours=[5, 6], debut=10, fin=14)]
    )

    assert windows[0].label == "Semaine"
    assert saved[0].label == "Week-end"
    assert fake_client.updated_fields["Cle"] == "availability_windows"
    assert "Week-end" in fake_client.updated_fields["Valeur"]
