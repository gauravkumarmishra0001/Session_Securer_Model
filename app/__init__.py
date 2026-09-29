from flask import Flask

from app.config import Config
from app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.models.user import User
    from app.models.session import Session

    from app.routes.auth import auth_bp
    from app.routes.sessions import sessions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(sessions_bp)

    with app.app_context():
        db.create_all()

    return app
