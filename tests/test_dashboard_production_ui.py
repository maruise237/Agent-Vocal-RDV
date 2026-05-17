from fastapi.testclient import TestClient

from main import app


def test_dashboard_uses_production_app_shell():
    client = TestClient(app)

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert 'class="app-frame"' in response.text
    assert 'href="#main-content"' in response.text
    assert 'role="status"' in response.text
    assert "Centre de contrôle" in response.text


def test_dashboard_template_is_not_inlined_in_router():
    with open("dashboard.py", encoding="utf-8") as dashboard_file:
        source = dashboard_file.read()

    assert "templates/dashboard.html" in source
    assert "<style>" not in source
