# Dashboard-first Dokploy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable FastAPI dashboard slice for Agent Vocal RDV, ready to run locally and deploy on Dokploy with Docker.

**Architecture:** A small FastAPI monolith serves dashboard HTML and JSON APIs. Appointment and availability behavior lives in focused service modules so Airtable and Google Calendar adapters can replace local storage later.

**Tech Stack:** Python, FastAPI, Pydantic, pytest, Docker, Dokploy.

---

### Task 1: Project Dependencies And Health Route

**Files:**
- Create: `requirements.txt`
- Create: `settings.py`
- Create: `main.py`
- Test: `tests/test_health.py`

- [ ] **Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient

from main import app


def test_health_route_returns_active_status():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "Agent Vocal RDV actif"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_health.py -v`

Expected: FAIL because `main` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `requirements.txt` with FastAPI, Uvicorn, Pydantic settings, pytest, and httpx. Create `settings.py` with environment settings. Create `main.py` with a FastAPI app and `GET /`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_health.py -v`

Expected: PASS.

### Task 2: Dashboard Authentication And HTML Route

**Files:**
- Create: `dashboard.py`
- Modify: `main.py`
- Test: `tests/test_dashboard_auth.py`

- [ ] **Step 1: Write failing tests**

```python
from fastapi.testclient import TestClient

from main import app


def test_dashboard_page_renders_login_shell():
    client = TestClient(app)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert "Agent Vocal RDV" in response.text
    assert "dashboard-root" in response.text


def test_appointments_api_rejects_invalid_password():
    client = TestClient(app)

    response = client.get("/api/appointments", headers={"X-Dashboard-Password": "bad"})

    assert response.status_code == 401
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_dashboard_auth.py -v`

Expected: FAIL because `/dashboard` and `/api/appointments` do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `dashboard.py` with an APIRouter, a `GET /dashboard` HTML response, a password checker using `X-Dashboard-Password`, and a temporary `GET /api/appointments` route.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_dashboard_auth.py -v`

Expected: PASS.

### Task 3: Appointment Models And Service

**Files:**
- Create: `models.py`
- Create: `services/__init__.py`
- Create: `services/appointments.py`
- Modify: `dashboard.py`
- Test: `tests/test_appointments.py`

- [ ] **Step 1: Write failing tests**

```python
from fastapi.testclient import TestClient

from main import app


VALID_HEADERS = {"X-Dashboard-Password": "change-me"}


def test_appointments_api_returns_expected_schema():
    client = TestClient(app)

    response = client.get("/api/appointments", headers=VALID_HEADERS)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["status"] == "Confirme"
    assert "email" in payload[0]
    assert "calendar_event_id" in payload[0]


def test_appointment_status_rejects_unknown_status():
    client = TestClient(app)

    response = client.patch(
        "/api/appointments/appt-1/status",
        headers=VALID_HEADERS,
        json={"status": "Inconnu"},
    )

    assert response.status_code == 422
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_appointments.py -v`

Expected: FAIL because schemas and status updates are not implemented.

- [ ] **Step 3: Write minimal implementation**

Add Pydantic models for appointment statuses, appointment records, and status update requests. Add a local appointment service with sample data and status update validation. Wire dashboard routes to the service.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_appointments.py -v`

Expected: PASS.

### Task 4: Availability Models And API

**Files:**
- Modify: `models.py`
- Create: `services/availability.py`
- Modify: `dashboard.py`
- Test: `tests/test_availability.py`

- [ ] **Step 1: Write failing tests**

```python
from fastapi.testclient import TestClient

from main import app


VALID_HEADERS = {"X-Dashboard-Password": "change-me"}


def test_availability_api_returns_default_windows():
    client = TestClient(app)

    response = client.get("/api/availability", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()[0]["label"] == "Semaine"


def test_availability_api_rejects_invalid_hours():
    client = TestClient(app)

    response = client.post(
        "/api/availability",
        headers=VALID_HEADERS,
        json=[{"id": "bad", "label": "Bad", "jours": [1], "debut": 18, "fin": 9}],
    )

    assert response.status_code == 422
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_availability.py -v`

Expected: FAIL because availability routes do not exist.

- [ ] **Step 3: Write minimal implementation**

Add availability models with validators, a local availability service, and `GET/POST /api/availability`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_availability.py -v`

Expected: PASS.

### Task 5: Dokploy Deployment Assets

**Files:**
- Create: `Dockerfile`
- Create: `.dockerignore`
- Create: `.env.example`
- Modify: `README.md`
- Test: full test suite

- [ ] **Step 1: Write deployment files**

Create a Python Docker image that installs `requirements.txt` and runs Uvicorn on port `8000`.

- [ ] **Step 2: Run all tests**

Run: `pytest -v`

Expected: PASS.

- [ ] **Step 3: Verify Docker config is present**

Run: `Get-Content Dockerfile`

Expected: Shows `EXPOSE 8000` and the Uvicorn command.
