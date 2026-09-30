
from app.services.event_service import (
    get_user_events
)

from app.services.feature_service import (
    build_user_profile,
    extract_session_features
)

from app.services.anomaly_service import (
    calculate_anomaly_score,
    classify_anomaly
)

from app.services.feature_engineering_service import (
    build_feature_vector
)

from app.services.isolation_forest_service import (
    predict_isolation_forest,
    load_isolation_forest
)

from app.services.risk_service import (
    calculate_ml_risk,
    classify_ml_risk
)


MINIMUM_HISTORY = 3


def analyze_session(session):

    events = get_user_events(
        session.user_id
    )

    historical_events = [
        event
        for event in events
        if event.session_id != session.id
    ]

    if len(historical_events) < MINIMUM_HISTORY:

        return {
            "user_id":
                session.user_id,

            "session_id":
                session.id,

            "profile_status":
                "INITIALIZING",

            "historical_events":
                len(historical_events),

            "minimum_required":
                MINIMUM_HISTORY,

            "classification":
                "INSUFFICIENT_HISTORY",

            "anomaly_score":
                None,

            "ml_available":
                False,

            "ml_risk_score":
                None,

            "ml_classification":
                "INSUFFICIENT_HISTORY"
        }

    profile = build_user_profile(
        historical_events
    )

    rule_features = extract_session_features(
        session,
        profile
    )

    rule_score = calculate_anomaly_score(
        rule_features
    )

    rule_classification = classify_anomaly(
        rule_score
    )

    feature_vector = build_feature_vector(
        session,
        historical_events
    )

    model_artifact = load_isolation_forest()

    result = {
        "user_id":
            session.user_id,

        "session_id":
            session.id,

        "profile_status":
            "READY",

        "historical_events":
            len(historical_events),

        "features":
            rule_features,

        "anomaly_score":
            rule_score,

        "classification":
            rule_classification,

        "feature_vector":
            feature_vector,

        "ml_available":
            False,

        "ml_risk_score":
            None,

        "ml_classification":
            "MODEL_UNAVAILABLE",

        "isolation_forest_prediction":
            None,

        "decision_score":
            None
    }

    if model_artifact is None:
        return result

    ml_result = predict_isolation_forest(
        feature_vector
    )

    ml_risk = calculate_ml_risk(
        ml_result["decision_score"],
        model_artifact["metadata"]
    )

    ml_classification = classify_ml_risk(
        ml_risk
    )

    result.update({
        "ml_available":
            True,

        "ml_risk_score":
            ml_risk,

        "ml_classification":
            ml_classification,

        "isolation_forest_prediction":
            ml_result["prediction"],

        "decision_score":
            ml_result["decision_score"]
    })

    return result
