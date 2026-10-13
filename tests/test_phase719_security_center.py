from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "app" / "routes" / "web.py"
SESSIONS = ROOT / "app" / "routes" / "sessions.py"
AUTH = ROOT / "app" / "routes" / "auth.py"
DASHBOARD = ROOT / "app" / "routes" / "dashboard.py"

def test_security_center_route_and_sections_exist():
    source = WEB.read_text(encoding="utf-8")
    assert re.search(
        r'@web_bp\.get\s*\(\s*["\']/security-center["\']',
        source
    )
    for required in (
        "Active sessions",
        "Login history",
        "Security alerts",
        "Security events",
        "Architecture and detection flow",
        "/api/sessions",
        "/api/dashboard/login-history",
        "/api/dashboard/security-alerts",
        "/api/social/events",
        "/api/auth/logout",
    ):
        assert required in source

def test_security_center_uses_safe_text_rendering():
    source = WEB.read_text(encoding="utf-8")
    page = source[source.rfind('@web_bp.get("/security-center")'):]
    assert "textContent" in page
    assert "createElement" in page
    assert "innerHTML" not in page

def test_session_revocation_route_keeps_auth_and_ownership_checks():
    source = SESSIONS.read_text(encoding="utf-8")
    match = re.search(
        r'@sessions_bp\.route\s*\(\s*'
        r'(["\'])/<int:session_id>\1\s*,\s*'
        r'methods\s*=\s*\[\s*["\']DELETE["\']\s*\]\s*\)',
        source,
        re.MULTILINE,
    )
    assert match
    body = source[match.end():]
    assert "get_current_session()" in body
    assert "current_session is None" in body
    assert "target.user_id != current_session.user_id" in body
    assert "revoke_session(target)" in body

def test_logout_revokes_resolved_session_and_deletes_cookie():
    source = AUTH.read_text(encoding="utf-8")
    start = source.find("def logout")
    assert start >= 0
    body = source[start:]
    assert "get_session_from_token" in body
    assert "revoke_session(session)" in body
    assert "delete_cookie" in body

def test_dashboard_history_and_alert_endpoints_still_exist():
    source = DASHBOARD.read_text(encoding="utf-8")
    assert "login-history" in source
    assert "security-alerts" in source
