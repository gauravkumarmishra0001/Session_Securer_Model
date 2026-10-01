
from datetime import datetime, timezone

from app.database import db


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class RiskAssessment(db.Model):
    __tablename__ = "risk_assessments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=True
    )

    classification = db.Column(
        db.String(50),
        nullable=True
    )

    ml_classification = db.Column(
        db.String(50),
        nullable=True
    )

    risk_score = db.Column(
        db.Float,
        nullable=True
    )

    anomaly_score = db.Column(
        db.Float,
        nullable=True
    )

    ml_risk_score = db.Column(
        db.Float,
        nullable=True
    )

    action = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now
    )

    user = db.relationship("User")
    session = db.relationship("Session")
