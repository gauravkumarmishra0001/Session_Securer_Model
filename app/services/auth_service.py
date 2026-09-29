import secrets

from datetime import timedelta

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.database import db
from app.models.user import User
from app.models.session import Session, utc_now


def normalize_email(email):
    if not email:
        return ""

    return email.strip().lower()


def create_user(username, email, password):
    username = username.strip()
    email = normalize_email(email)

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return None

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return None

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return user


def authenticate_user(email, password):
    email = normalize_email(email)

    user = User.query.filter_by(
        email=email
    ).first()

    if user is None:
        return None

    if not check_password_hash(
        user.password_hash,
        password
    ):
        return None

    return user


def create_session(
    user,
    ip_address,
    user_agent,
    device_info,
    ttl_seconds
):
    raw_token = secrets.token_urlsafe(32)

    now = utc_now()

    session = Session(
        user_id=user.id,
        token_hash=Session.hash_token(
            raw_token
        ),
        ip_address=ip_address,
        user_agent=user_agent,
        device_type=device_info.get(
            "device_type",
            "Unknown"
        ),
        browser=device_info.get(
            "browser",
            "Unknown"
        ),
        operating_system=device_info.get(
            "operating_system",
            "Unknown"
        ),
        created_at=now,
        last_seen_at=now,
        expires_at=now + timedelta(
            seconds=ttl_seconds
        )
    )

    db.session.add(session)
    db.session.commit()

    return raw_token, session


def revoke_session(session):
    session.revoke()
    db.session.commit()


def revoke_all_user_sessions(user):
    sessions = Session.query.filter_by(
        user_id=user.id
    ).all()

    now = utc_now()

    for session in sessions:
        session.revoked_at = now

    db.session.commit()

    return len(sessions)
