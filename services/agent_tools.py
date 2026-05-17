from services.appointments import appointment_service
from services.availability import availability_service
from services.google_calendar_service import build_configured_google_calendar_service


DAY_NAMES = {
    0: "lundi",
    1: "mardi",
    2: "mercredi",
    3: "jeudi",
    4: "vendredi",
    5: "samedi",
    6: "dimanche",
}


def verifier_disponibilites(jours: int = 7) -> str:
    windows = availability_service.list_windows()
    if not windows:
        return "Aucun créneau disponible n'est configuré pour le moment."

    lines = []
    for window in windows:
        day_labels = ", ".join(DAY_NAMES[day] for day in window.jours)
        lines.append(f"{window.label}: {day_labels}, de {window.debut}h à {window.fin}h")

    return f"Créneaux disponibles sur les {jours} prochains jours : " + " ; ".join(lines)


def reserver_creneau(
    prenom: str,
    nom: str,
    email: str,
    date_rdv: str,
    besoin: str,
    call_id: str | None = None,
) -> str:
    calendar_event_id = None
    calendar = build_configured_google_calendar_service()
    if calendar:
        calendar_event_id = calendar.book_appointment(
            first_name=prenom,
            last_name=nom,
            email=email,
            date_rdv=date_rdv,
            besoin=besoin,
        )

    appointment = appointment_service.create_appointment(
        first_name=prenom,
        last_name=nom,
        email=email,
        date_rdv=date_rdv,
        besoin=besoin,
        call_id=call_id,
        calendar_event_id=calendar_event_id,
    )

    return (
        f"Rendez-vous confirmé pour {appointment.first_name} {appointment.last_name} "
        f"le {appointment.date_rdv}. Email confirmé : {appointment.email}."
    )
