from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import HTMLResponse

from models import Appointment, AppointmentStatusUpdate, AvailabilityWindow
from services.appointments import appointment_service
from services.availability import availability_service
from services.google_calendar_service import build_configured_google_calendar_service
from settings import get_settings


router = APIRouter()
TEMPLATE_PATH = Path(__file__).parent / "templates/dashboard.html"


def require_dashboard_password(
    x_dashboard_password: Annotated[str | None, Header()] = None,
) -> None:
    if x_dashboard_password != get_settings().dashboard_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe dashboard invalide",
        )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")


@router.get("/api/appointments")
def list_appointments(
    _: Annotated[None, Depends(require_dashboard_password)],
) -> list[Appointment]:
    return appointment_service.list_appointments()


@router.patch("/api/appointments/{appointment_id}/status")
def update_appointment_status(
    appointment_id: str,
    payload: AppointmentStatusUpdate,
    _: Annotated[None, Depends(require_dashboard_password)],
) -> Appointment:
    appointment = appointment_service.update_status(appointment_id, payload.status)
    if payload.status == "Annule" and appointment.calendar_event_id:
        calendar = build_configured_google_calendar_service()
        if calendar:
            calendar.cancel_event(appointment.calendar_event_id)
    return appointment


@router.get("/api/availability")
def list_availability(
    _: Annotated[None, Depends(require_dashboard_password)],
) -> list[AvailabilityWindow]:
    return availability_service.list_windows()


@router.post("/api/availability")
def save_availability(
    windows: list[AvailabilityWindow],
    _: Annotated[None, Depends(require_dashboard_password)],
) -> list[AvailabilityWindow]:
    return availability_service.save_windows(windows)
