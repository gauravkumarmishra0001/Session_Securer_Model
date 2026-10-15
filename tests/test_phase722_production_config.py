import pytest

from app import create_app


def test_production_rejects_missing_explicit_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("FLASK_ENVIRONMENT", raising=False)
    monkeypatch.delenv("FLASK_CONFIG", raising=False)
    monkeypatch.delenv("SESSION_SECURER_SECRET_KEY", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///unused-test.db")

    with pytest.raises(RuntimeError, match="strong, explicitly configured secret"):
        create_app()


def test_production_rejects_short_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("FLASK_ENVIRONMENT", raising=False)
    monkeypatch.delenv("FLASK_CONFIG", raising=False)
    monkeypatch.setenv("SESSION_SECURER_SECRET_KEY", "too-short")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///unused-test.db")

    with pytest.raises(RuntimeError, match="at least 32 characters"):
        create_app()


def test_production_requires_database_url(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("FLASK_ENVIRONMENT", raising=False)
    monkeypatch.delenv("FLASK_CONFIG", raising=False)
    monkeypatch.setenv(
        "SESSION_SECURER_SECRET_KEY",
        "this-is-a-test-secret-that-is-long-enough-123456"
    )
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="requires DATABASE_URL"):
        create_app()
