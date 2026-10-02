import os

from flask import Flask, request

from app.config import Config
from app.database import db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.config["SECRET_KEY"] = os.environ.get(
        "SESSION_SECURER_SECRET_KEY",
        app.config.get("SECRET_KEY")
    )

    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    if os.environ.get("SESSION_SECURER_SECURE_COOKIES") == "1":
        app.config["SESSION_COOKIE_SECURE"] = True

    db.init_app(app)

    # Existing models
    from app.models.user import User
    from app.models.session import Session
    from app.models.session_event import SessionEvent
    from app.models.otp_challenge import OTPChallenge
    from app.models.risk_assessment import RiskAssessment
    from app.models.security_alert import SecurityAlert

    # Phase 6 models
    from app.models.social_account import SocialAccount
    from app.models.social_event import SocialEvent

    # Existing routes
    from app.routes.auth import auth_bp
    from app.routes.sessions import sessions_bp
    from app.routes.detection import detection_bp
    from app.routes.prevention import prevention_bp
    from app.routes.dashboard import dashboard_bp

    # Phase 6 routes
    from app.routes.social import social_bp
    from app.routes.web import web_bp

    # Register existing routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(prevention_bp)
    app.register_blueprint(dashboard_bp)

    # Register Phase 6 routes
    app.register_blueprint(social_bp)
    app.register_blueprint(web_bp)

    @app.after_request
    def add_security_headers(response):

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["Referrer-Policy"] = (
            "strict-origin-when-cross-origin"
        )

        response.headers["Permissions-Policy"] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=()"
        )

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

        if request.is_secure:

            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response

    with app.app_context():
        db.create_all()

    return app
