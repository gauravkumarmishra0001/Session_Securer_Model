
from datetime import datetime, timezone
import hashlib

from app.database import db


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class OTPChallenge(db.Model):
    __tablename__ = "otp_challenges"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    otp_hash = db.Column(
        db.String(64),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    used_at = db.Column(
        db.DateTime,
        nullable=True
    )

    @staticmethod
    def hash_otp(otp):
        return hashlib.sha256(
            str(otp).encode("utf-8")
        ).hexdigest()

    @property
    def active(self):
        now = utc_now()

        return (
            self.used_at is None
            and self.expires_at is not None
            and self.expires_at > now
        )

    def mark_used(self):
        self.used_at = utc_now()
