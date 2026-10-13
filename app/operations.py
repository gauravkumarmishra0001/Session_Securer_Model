"""Operational safeguards for Session Securer Model."""

import logging
import os

from flask import jsonify, request
from werkzeug.exceptions import HTTPException


def configure_phase722_operations(app):
    """Configure environment, logging, health probes, and safe errors."""

    environment = (
        os.getenv("APP_ENV")
        or os.getenv("FLASK_ENVIRONMENT")
        or os.getenv("FLASK_CONFIG")
        or "development"
    ).strip().lower()
    production = environment in {"production", "prod"}

    secret = os.getenv("SECRET_KEY") or os.getenv("FLASK_SECRET_KEY")
    if secret:
        app.config["SECRET_KEY"] = secret
    elif not app.config.get("SECRET_KEY"):
        if production:
            raise RuntimeError(
                "Production startup requires SECRET_KEY or FLASK_SECRET_KEY."
            )
        app.config["SECRET_KEY"] = os.urandom(32).hex()
        app.logger.warning(
            "No secret key supplied; using an ephemeral development key."
        )

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = "postgresql://" + database_url[len("postgres://"):]
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    if production:
        app.config["SESSION_COOKIE_SECURE"] = True
        app.config["SESSION_COOKIE_HTTPONLY"] = True
        app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    if not app.logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        ))
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO if production else logging.DEBUG)

    def database_ready():
        if "sqlalchemy" not in app.extensions:
            return True
        try:
            from sqlalchemy import text
            extension = app.extensions["sqlalchemy"]
            with app.app_context():
                extension.session.execute(text("SELECT 1"))
            return True
        except Exception:
            app.logger.error("Readiness database probe failed.")
            return False

    existing_paths = {rule.rule for rule in app.url_map.iter_rules()}

    if "/health/live" not in existing_paths:
        @app.get("/health/live", endpoint="phase722_health_live")
        def phase722_health_live():
            return jsonify({"status": "ok"}), 200

    if "/health/ready" not in existing_paths:
        @app.get("/health/ready", endpoint="phase722_health_ready")
        def phase722_health_ready():
            if not database_ready():
                return jsonify({"status": "not_ready"}), 503
            return jsonify({"status": "ready"}), 200

    @app.errorhandler(500)
    def phase722_internal_error(error):
        app.logger.error("Unhandled internal server error.")
        if request.accept_mimetypes.best == "application/json":
            return jsonify({"error": "internal_server_error"}), 500
        return "An internal server error occurred.", 500

    @app.errorhandler(HTTPException)
    def phase722_http_error(error):
        status = error.code or 500
        if request.accept_mimetypes.best == "application/json":
            return jsonify({
                "error": error.name.lower().replace(" ", "_")
            }), status
        return error.name, status

    return app
