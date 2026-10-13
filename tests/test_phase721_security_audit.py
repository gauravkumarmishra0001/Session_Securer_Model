from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "app" / "routes"

def route_sources():
    return {
        path: path.read_text(encoding="utf-8")
        for path in ROUTES.glob("*.py")
    }

def combined_source():
    return "\n".join(route_sources().values())

def test_all_route_modules_parse_as_python():
    for path, source in route_sources().items():
        ast.parse(source, filename=str(path))

def test_session_revocation_has_authentication_and_authorization_guards():
    source = combined_source()
    assert re.search(r"\brevoke_session\s*\(", source)
    assert re.search(r"\b401\b", source)
    assert re.search(r"\b403\b", source)

def test_logout_and_session_revocation_paths_are_present():
    source = combined_source()
    assert re.search(r"\blogout\b", source, re.IGNORECASE)
    assert re.search(r"\brevoke_session\s*\(", source)

def test_phase720_privacy_routes_remain_present():
    source = combined_source()
    assert re.search(r'@web_bp\.get\(["\']/terms["\']\)', source)
    assert re.search(r'@web_bp\.get\(["\']/privacy["\']\)', source)

def test_phase720_security_center_remains_present():
    source = combined_source()
    assert re.search(r'@web_bp\.get\(["\']/security-center["\']\)', source)

def test_phase721_audit_documentation_is_present():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Phase 7.21" in readme
    assert "CSRF" in readme
    assert "rate limiting" in readme.lower()
