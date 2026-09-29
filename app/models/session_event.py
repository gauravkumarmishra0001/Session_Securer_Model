from datetime import datetime, timezone

from app.database import db


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class SessionEvent(db.Model):
    __tablename__ = "session_events"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=False
    )

    event_type = db.Column(
        db.String(50),
        nullable=False
    )

    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    device_type = db.Column(
        db.String(50),
        nullable=True
    )

    browser = db.Column(
        db.String(100),
        nullable=True
    )

    operating_system = db.Column(
        db.String(100),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "session_events",
            lazy=True
        )
    )

    session = db.relationship(
        "Session",
        backref=db.backref(
            "events",
            lazy=True
        )
    )
