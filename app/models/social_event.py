from datetime import datetime
from app.database import db


class SocialEvent(db.Model):
    __tablename__ = "social_events"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    social_account_id = db.Column(
        db.Integer,
        db.ForeignKey("social_accounts.id"),
        nullable=True,
        index=True
    )

    event_type = db.Column(db.String(64), nullable=False)
    platform = db.Column(db.String(64), nullable=False)

    ip_address = db.Column(db.String(128), nullable=True)
    device_type = db.Column(db.String(128), nullable=True)
    browser = db.Column(db.String(128), nullable=True)
    operating_system = db.Column(db.String(128), nullable=True)
    location = db.Column(db.String(255), nullable=True)

    risk_score = db.Column(db.Float, nullable=True)

    classification = db.Column(
        db.String(64),
        nullable=False
    )

    action = db.Column(
        db.String(64),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "social_account_id": self.social_account_id,
            "event_type": self.event_type,
            "platform": self.platform,
            "ip_address": self.ip_address,
            "device_type": self.device_type,
            "browser": self.browser,
            "operating_system": self.operating_system,
            "location": self.location,
            "risk_score": self.risk_score,
            "classification": self.classification,
            "action": self.action,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }
