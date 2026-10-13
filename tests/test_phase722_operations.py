import importlib.util
from pathlib import Path
from flask import Flask


def load_module():
    path = Path(__file__).resolve().parents[1] / "app" / "operations.py"
    spec = importlib.util.spec_from_file_location("phase722_test_module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_health_routes(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    module = load_module()
    app = Flask(__name__)
    module.configure_phase722_operations(app)
    client = app.test_client()

    assert client.get("/health/live").status_code == 200
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ready"}


def test_production_requires_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)

    module = load_module()
    app = Flask(__name__)
    app.config.pop("SECRET_KEY", None)

    try:
        module.configure_phase722_operations(app)
    except RuntimeError as exc:
        assert "requires SECRET_KEY" in str(exc)
    else:
        raise AssertionError("Production must require an explicit secret.")


def test_database_url_override(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.setenv("SECRET_KEY", "test-only-secret")
    monkeypatch.setenv("DATABASE_URL", "postgres://example.invalid/testdb")

    module = load_module()
    app = Flask(__name__)
    module.configure_phase722_operations(app)

    assert app.config["SQLALCHEMY_DATABASE_URI"] == (
        "postgresql://example.invalid/testdb"
    )


def test_production_cookie_flags(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("SECRET_KEY", "test-only-secret")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    module = load_module()
    app = Flask(__name__)
    module.configure_phase722_operations(app)

    assert app.config["SESSION_COOKIE_SECURE"] is True
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
