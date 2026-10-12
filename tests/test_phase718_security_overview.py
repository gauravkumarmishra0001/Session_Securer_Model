"""PHASE718_OVERVIEW_REGRESSION_TESTS

Regression checks for the Phase 7.18 security overview and dashboard.
"""
from pathlib import Path

from app import create_app


def make_client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_security_overview_route_and_accessible_states():
    response = make_client().get("/security-overview")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="status"' in html
    assert 'aria-live="polite"' in html
    assert 'id="summary"' in html
    assert 'id="sessions"' in html
    assert 'id="alerts"' in html
    assert "renderSummaryPanel" in html
    assert "textContent" in html


def test_security_headers_are_present_on_overview():
    response = make_client().get("/security-overview")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Referrer-Policy") == (
        "strict-origin-when-cross-origin"
    )
    csp = response.headers.get("Content-Security-Policy", "")
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert "base-uri 'self'" in csp


def test_dashboard_api_endpoints_require_authentication():
    client = make_client()
    endpoints = [
        "/api/dashboard/summary",
        "/api/dashboard/active-sessions",
        "/api/dashboard/login-history",
        "/api/dashboard/risk-scores",
        "/api/dashboard/blocked-attempts",
        "/api/dashboard/security-alerts",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 401, (
            f"{endpoint} should require authentication; "
            f"received {response.status_code}"
        )


def test_dashboard_section_css_uses_dark_contrast():
    source = (
        Path(__file__).resolve().parent.parent
        / "app" / "routes" / "dashboard.py"
    ).read_text(encoding="utf-8")
    assert "background: #17221e;" in source
    assert "color: #e8f0ec;" in source
    assert "border: 1px solid #40544a;" in source
    assert "background: white;" not in source


def test_dashboard_table_values_are_html_escaped():
    source = (
        Path(__file__).resolve().parent.parent
        / "app" / "routes" / "dashboard.py"
    ).read_text(encoding="utf-8")
    assert "function safe(value)" in source
    assert 'replace(/[&<>"\']/g' in source
    assert "return entities[character]" in source
