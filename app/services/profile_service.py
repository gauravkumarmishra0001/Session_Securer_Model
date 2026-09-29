from app.services.event_service import get_user_events
from app.services.feature_service import build_user_profile


def get_user_profile(user_id):
    """
    Return the behavioral profile of a user.
    """

    events = get_user_events(user_id)

    profile = build_user_profile(events)

    return profile
