from fastapi import HTTPException, status

from models import Appointment, AppointmentStatus
from services.airtable_client import AirtableClient
from services.airtable_repositories import AirtableAppointmentRepository
from settings import get_settings


class AppointmentService:
    def __init__(self) -> None:
        self._appointments: dict[str, Appointment] = {
            "appt-1": Appointment(
                id="appt-1",
                first_name="Camille",
                last_name="Durand",
                email="camille@example.com",
                date_rdv="2026-05-18 09:00",
                besoin="Découvrir l'offre agent vocal",
                status=AppointmentStatus.CONFIRME,
                created_at="2026-05-17T10:00:00",
                call_id="call-demo-1",
                calendar_event_id="calendar-demo-1",
            )
        }

    def list_appointments(self) -> list[Appointment]:
        return list(self._appointments.values())

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
        appointment_id = f"appt-{len(self._appointments) + 1}"
        appointment = Appointment(
            id=appointment_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_rdv=date_rdv,
            besoin=besoin,
            status=AppointmentStatus.CONFIRME,
            created_at="2026-05-17T00:00:00",
            call_id=call_id,
            calendar_event_id=calendar_event_id,
        )
        self._appointments[appointment_id] = appointment
        return appointment

    def update_status(
        self, appointment_id: str, new_status: AppointmentStatus
    ) -> Appointment:
        appointment = self._appointments.get(appointment_id)
        if appointment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rendez-vous introuvable",
            )

        updated = appointment.model_copy(update={"status": new_status})
        self._appointments[appointment_id] = updated
        return updated


def build_appointment_service():
    settings = get_settings()
    if settings.airtable_api_key and settings.airtable_base_id:
        return AirtableAppointmentRepository(
            AirtableClient(settings.airtable_api_key, settings.airtable_base_id),
            settings.airtable_appointments_table,
        )
    return AppointmentService()


appointment_service = build_appointment_service()
