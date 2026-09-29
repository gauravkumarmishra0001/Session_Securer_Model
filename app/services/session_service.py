from app.database import db

from app.models.session import (
    Session,
    utc_now
)


def get_session_from_token(token):
    if not token:
        return None

    token_hash = Session.hash_token(token)

    session = Session.query.filter_by(
        token_hash=token_hash
    ).first()

    if session is None:
        return None

    if not session.active:
        return None

    return session


def update_last_seen(session):
    session.last_seen_at = utc_now()
    db.session.commit()


def revoke_session(session):
    session.revoke()
    db.session.commit()


def get_active_sessions_for_user(user_id):
    sessions = Session.query.filter_by(
        user_id=user_id
    ).all()

    return [
        session
        for session in sessions
        if session.active
    ]


def session_to_dict(session):
    return {
        "id": session.id,
        "user_id": session.user_id,
        "ip_address": session.ip_address,
        "user_agent": session.user_agent,
        "device_type": session.device_type,
        "browser": session.browser,
        "operating_system": session.operating_system,
        "created_at": (
            session.created_at.isoformat()
            if session.created_at
            else None
        ),
        "last_seen_at": (
            session.last_seen_at.isoformat()
            if session.last_seen_at
            else None
        ),
        "expires_at": (
            session.expires_at.isoformat()
            if session.expires_at
            else None
        ),
        "revoked_at": (
            session.revoked_at.isoformat()
            if session.revoked_at
            else None
        ),
        "active": session.active
    }
