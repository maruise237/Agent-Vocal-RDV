# Dashboard-first Dokploy Design

## Goal

Build the first functional slice of the Agent Vocal RDV project around the web dashboard. The app must run locally, be testable, and be ready for deployment on Dokploy through Docker. VAPI, Google Calendar, and Airtable integrations will be added behind stable service boundaries after the dashboard foundation is working.

## Scope

This first slice includes:

- A FastAPI application with health and dashboard routes.
- A password-protected dashboard at `/dashboard`.
- JSON APIs for appointments and availability settings.
- Local in-memory or file-backed service implementations for development.
- Service interfaces that can later be replaced by Airtable and Google Calendar implementations.
- Docker deployment assets for Dokploy.
- Automated tests for the main routes and service behavior.

This slice does not include:

- Live VAPI phone calls.
- Real Google Calendar writes.
- Real Airtable records.
- Public domain configuration inside Dokploy.

## Architecture

The project will be a Python FastAPI monolith:

- `main.py` creates the FastAPI app, registers routers, and exposes health checks.
- `dashboard.py` owns dashboard HTML and dashboard API routes.
- `services/appointments.py` owns appointment listing and status changes.
- `services/availability.py` owns business availability rules.
- `models.py` defines shared Pydantic models.
- `settings.py` reads environment variables.
- `tests/` covers route behavior and service behavior.

This keeps the first version simple while preserving clean boundaries for later Airtable and Calendar adapters.

## Dashboard Behavior

`GET /dashboard` returns the dashboard HTML. Access is controlled by a password configured through `DASHBOARD_PASSWORD`.

For the first version, authentication will be lightweight:

- The dashboard page asks for the password in the browser.
- API calls include the password in an `X-Dashboard-Password` header.
- The backend rejects missing or invalid passwords with `401`.

This is enough for the MVP and can later be replaced with sessions or signed tokens if needed.

## API Behavior

`GET /` returns a simple health payload.

`GET /api/appointments` returns a list of appointments with fields for customer name, email, date, need, status, call id, and future calendar event id.

`PATCH /api/appointments/{id}/status` changes an appointment status. For now, it updates the local service only. Later, when status becomes `Annule`, the Calendar adapter can delete the matching event.

`GET /api/availability` returns availability windows.

`POST /api/availability` saves availability windows after validating day and hour ranges.

## Data Model

Appointments use these statuses:

- `Confirme`
- `Annule`
- `Termine`

Availability windows contain:

- `id`
- `label`
- `jours`, where Monday is `0` and Sunday is `6`
- `debut`, hour from `0` to `23`
- `fin`, hour from `1` to `24`, greater than `debut`

## Dokploy Deployment

The app will include:

- `Dockerfile`
- `.dockerignore`
- `.env.example`
- `requirements.txt`

The container will run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Dokploy should expose port `8000` and provide environment variables, starting with `DASHBOARD_PASSWORD`.

## Testing

Implementation should follow TDD:

- Add a failing test for each route or service behavior.
- Verify the test fails for the expected reason.
- Add the minimal implementation.
- Verify the test passes.

Initial test coverage:

- Health route returns active status.
- Dashboard rejects invalid password.
- Appointments API rejects invalid password.
- Appointments API returns the expected schema with valid password.
- Availability API validates hour and day ranges.
- Appointment status updates reject unknown statuses.

## Future Integrations

After this slice, the next implementation slices can add:

- Airtable-backed appointment and config services.
- Google Calendar booking and cancellation service.
- VAPI webhook route and tool dispatch.
- Dokploy API deployment automation.
