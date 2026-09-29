from app.database import db
from app.models.session_event import SessionEvent


def record_login_event(session):
    event = SessionEvent(
        user_id=session.user_id,
        session_id=session.id,
        event_type="LOGIN",
        ip_address=session.ip_address,
        device_type=session.device_type,
        browser=session.browser,
        operating_system=session.operating_system
    )

    db.session.add(event)
    db.session.commit()

    return event


def get_user_events(user_id):
    return (
        SessionEvent.query
        .filter_by(user_id=user_id)
        .order_by(SessionEvent.created_at.asc())
        .all()
    )
