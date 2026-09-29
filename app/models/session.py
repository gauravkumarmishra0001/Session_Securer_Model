import hashlib

from datetime import datetime, timezone

from app.database import db


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def normalize_datetime(value):
    if value is None:
        return None

    if value.tzinfo is not None:
        return value.astimezone(
            timezone.utc
        ).replace(tzinfo=None)

    return value


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    token_hash = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    user_agent = db.Column(
        db.Text,
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

    last_seen_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    revoked_at = db.Column(
        db.DateTime,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "sessions",
            lazy=True
        )
    )

    @staticmethod
    def hash_token(token):
        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    @property
    def active(self):
        now = utc_now()

        expires = normalize_datetime(
            self.expires_at
        )

        revoked = normalize_datetime(
            self.revoked_at
        )

        return (
            revoked is None
            and expires is not None
            and expires > now
        )

    def revoke(self):
        self.revoked_at = utc_now()
