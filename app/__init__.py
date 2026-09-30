
from flask import Flask

from app.config import Config
from app.database import db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    # Import models.
    from app.models.user import User
    from app.models.session import Session
    from app.models.session_event import SessionEvent
    from app.models.otp_challenge import OTPChallenge

    # Import routes.
    from app.routes.auth import auth_bp
    from app.routes.sessions import sessions_bp
    from app.routes.detection import detection_bp
    from app.routes.prevention import prevention_bp

    # Register routes.
    app.register_blueprint(auth_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(detection_bp)
    app.register_blueprint(prevention_bp)

    # Create missing database tables.
    with app.app_context():
        db.create_all()

    return app
