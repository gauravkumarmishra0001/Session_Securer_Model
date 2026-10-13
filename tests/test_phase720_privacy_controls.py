from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WEB = (ROOT / "app" / "routes" / "web.py").read_text(encoding="utf-8")

def test_phase720_terms_and_privacy_routes_exist():
    assert re.search(r'@web_bp\.get\(["\']/terms["\']\)', WEB)
    assert re.search(r'@web_bp\.get\(["\']/privacy["\']\)', WEB)
    assert "def phase720_terms" in WEB
    assert "def phase720_privacy" in WEB

def test_phase720_policy_pages_include_required_topics():
    for phrase in (
        "Acceptable use",
        "Security limitations",
        "Retention and access",
        "Sharing and third parties",
        "Your choices",
    ):
        assert phrase in WEB

def test_phase720_privacy_controls_are_accessible():
    for phrase in (
        'aria-labelledby="p720-controls-title"',
        'aria-live="polite"',
        'for="p720-telemetry"',
        'id="p720-check-permissions"',
        'id="p720-location"',
        'id="p720-notifications"',
    ):
        assert phrase in WEB

def test_phase720_api_data_is_not_inserted_as_html():
    # The new privacy-page script uses textContent/createElement for displayed
    # status strings and permission results, not innerHTML.
    start = WEB.index("# PHASE_7_20_PRIVACY_CONTROLS")
    section = WEB[start:]
    assert "textContent" in section
    assert "createElement" in section
    assert "innerHTML" not in section

def test_phase720_browser_preference_does_not_claim_server_enforcement():
    start = WEB.index("# PHASE_7_20_PRIVACY_CONTROLS")
    section = WEB[start:]
    assert "does not disable server-side logging" in section
    assert "does not change server-side logging or network requests" in section

def test_phase720_security_headers_are_set():
    start = WEB.index("# PHASE_7_20_PRIVACY_CONTROLS")
    section = WEB[start:]
    for header in (
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Cache-Control",
        "Permissions-Policy",
    ):
        assert header in section
