from datetime import datetime
from app.database import db


class SocialAccount(db.Model):
    __tablename__ = "social_accounts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    platform = db.Column(db.String(64), nullable=False)
    platform_user_id = db.Column(db.String(255), nullable=False)

    display_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)

    connected_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    last_used_at = db.Column(db.DateTime, nullable=True)

    active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "platform",
            "platform_user_id",
            name="uq_social_platform_user"
        ),
    )

    def __repr__(self):
        return f"<SocialAccount {self.platform}:{self.platform_user_id}>"
