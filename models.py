from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field, model_validator


class AppointmentStatus(StrEnum):
    CONFIRME = "Confirme"
    ANNULE = "Annule"
    TERMINE = "Termine"


class Appointment(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    date_rdv: str
    besoin: str
    status: AppointmentStatus
    created_at: str
    call_id: str | None = None
    calendar_event_id: str | None = None


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AvailabilityWindow(BaseModel):
    id: str
    label: str
    jours: list[int] = Field(min_length=1)
    debut: int = Field(ge=0, le=23)
    fin: int = Field(ge=1, le=24)

    @model_validator(mode="after")
    def validate_window(self) -> "AvailabilityWindow":
        if any(day < 0 or day > 6 for day in self.jours):
            raise ValueError("Les jours doivent être compris entre 0 et 6")
        if self.fin <= self.debut:
            raise ValueError("L'heure de fin doit être après l'heure de début")
        return self
