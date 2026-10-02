from datetime import datetime

from app.database import db
from app.models.user import User
from app.models.social_account import SocialAccount
from app.models.social_event import SocialEvent


DEMO_PLATFORM = "Simulated Social Platform"


def get_demo_user():
    return User.query.order_by(User.id.asc()).first()


def create_simulated_account(user):

    account = SocialAccount.query.filter_by(
        user_id=user.id,
        platform=DEMO_PLATFORM
    ).first()

    if account is None:

        account = SocialAccount(
            user_id=user.id,
            platform=DEMO_PLATFORM,
            platform_user_id=f"demo-user-{user.id}",
            display_name=user.username,
            email=user.email,
            connected_at=datetime.utcnow(),
            last_used_at=datetime.utcnow(),
            active=True
        )

        db.session.add(account)
        db.session.flush()

    else:

        account.last_used_at = datetime.utcnow()
        account.active = True

    return account


def record_social_event(
    user,
    account,
    event_type,
    device_type,
    browser,
    operating_system,
    location,
    risk_score,
    classification,
    action,
    ip_address="127.0.0.1"
):

    event = SocialEvent(
        user_id=user.id,
        social_account_id=account.id,
        event_type=event_type,
        platform=DEMO_PLATFORM,
        ip_address=ip_address,
        device_type=device_type,
        browser=browser,
        operating_system=operating_system,
        location=location,
        risk_score=float(risk_score),
        classification=classification,
        action=action,
        created_at=datetime.utcnow()
    )

    db.session.add(event)
    db.session.commit()

    return event


def simulate_normal_login():

    user = get_demo_user()

    if user is None:
        return None

    account = create_simulated_account(user)

    return record_social_event(
        user=user,
        account=account,
        event_type="SOCIAL_LOGIN",
        device_type="Desktop",
        browser="Chrome",
        operating_system="Windows",
        location="Known location",
        risk_score=0.05,
        classification="NORMAL",
        action="ALLOW"
    )


def simulate_new_device():

    user = get_demo_user()

    if user is None:
        return None

    account = create_simulated_account(user)

    return record_social_event(
        user=user,
        account=account,
        event_type="NEW_DEVICE_LOGIN",
        device_type="Mobile",
        browser="Safari",
        operating_system="iOS",
        location="Unusual location",
        risk_score=0.65,
        classification="UNUSUAL",
        action="VERIFY"
    )


def simulate_high_risk_login():

    user = get_demo_user()

    if user is None:
        return None

    account = create_simulated_account(user)

    return record_social_event(
        user=user,
        account=account,
        event_type="HIGH_RISK_LOGIN",
        device_type="Unknown device",
        browser="Unknown",
        operating_system="Unknown",
        location="Untrusted location",
        risk_score=0.95,
        classification="HIGH_RISK",
        action="BLOCK"
    )


def get_recent_events(limit=25):

    events = (
        SocialEvent.query
        .order_by(SocialEvent.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        event.to_dict()
        for event in events
    ]
