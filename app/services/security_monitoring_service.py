
from app.database import db

from app.models.risk_assessment import RiskAssessment
from app.models.security_alert import SecurityAlert


def to_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def calculate_risk_score(result):
    if not result:
        return None

    direct = to_float(
        result.get("risk_score")
    )

    if direct is not None:
        return round(direct, 4)

    scores = []

    anomaly = to_float(
        result.get("anomaly_score")
    )

    ml_risk = to_float(
        result.get("ml_risk_score")
    )

    if anomaly is not None:
        scores.append(anomaly)

    if ml_risk is not None:
        scores.append(ml_risk)

    if not scores:
        return None

    return round(max(scores), 4)


def record_security_decision(
    session,
    result,
    action
):
    result = result or {}

    risk_score = calculate_risk_score(result)

    assessment = RiskAssessment(
        user_id=session.user_id,
        session_id=session.id,
        classification=result.get(
            "classification"
        ),
        ml_classification=result.get(
            "ml_classification"
        ),
        risk_score=risk_score,
        anomaly_score=to_float(
            result.get("anomaly_score")
        ),
        ml_risk_score=to_float(
            result.get("ml_risk_score")
        ),
        action=action
    )

    db.session.add(assessment)

    classification = result.get(
        "classification"
    )

    ml_classification = result.get(
        "ml_classification"
    )

    suspicious = (
        action != "ALLOW"
        or classification in (
            "UNUSUAL",
            "HIGH_RISK",
            "HIGH_ANOMALY"
        )
        or ml_classification in (
            "UNUSUAL",
            "HIGH_RISK"
        )
    )

    if suspicious:

        if action == "BLOCK":
            severity = "HIGH"
        elif action == "VERIFY":
            severity = "MEDIUM"
        else:
            severity = "LOW"

        alert = SecurityAlert(
            user_id=session.user_id,
            session_id=session.id,
            alert_type="LOGIN_RISK",
            severity=severity,
            title="Suspicious login activity",
            message=(
                "Classification="
                + str(classification)
                + "; ML classification="
                + str(ml_classification)
                + "; risk_score="
                + str(risk_score)
            ),
            action=action
        )

        db.session.add(alert)

    db.session.commit()

    return assessment
