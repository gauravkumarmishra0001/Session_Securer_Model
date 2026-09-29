from app.services.event_service import get_user_events

from app.services.feature_service import (
    build_user_profile,
    extract_session_features
)

from app.services.anomaly_service import (
    calculate_anomaly_score,
    classify_anomaly
)


MINIMUM_HISTORY = 3


def analyze_session(session):
    """
    Analyze a session using the user's historical behavior.
    """

    events = get_user_events(session.user_id)

    historical_events = [
        event
        for event in events
        if event.session_id != session.id
    ]

    history_count = len(historical_events)

    # Do not make a security decision
    # without enough historical data.
    if history_count < MINIMUM_HISTORY:
        return {
            "user_id": session.user_id,
            "session_id": session.id,
            "profile_status": "INITIALIZING",
            "historical_events": history_count,
            "minimum_required": MINIMUM_HISTORY,
            "classification": "INSUFFICIENT_HISTORY",
            "anomaly_score": None
        }

    profile = build_user_profile(
        historical_events
    )

    features = extract_session_features(
        session,
        profile
    )

    score = calculate_anomaly_score(
        features
    )

    classification = classify_anomaly(
        score
    )

    return {
        "user_id": session.user_id,
        "session_id": session.id,
        "profile_status": "READY",
        "historical_events": history_count,
        "features": features,
        "anomaly_score": score,
        "classification": classification
    }
