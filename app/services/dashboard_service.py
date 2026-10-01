
from app.models.session import Session
from app.models.session_event import SessionEvent
from app.models.risk_assessment import RiskAssessment
from app.models.security_alert import SecurityAlert


def iso(value):
    if value is None:
        return None

    return value.isoformat()


def location_from_ip(ip):
    if not ip:
        return "Unknown"

    private_prefixes = (
        "127.",
        "10.",
        "192.168.",
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31."
    )

    if ip.startswith(private_prefixes):
        return "Private / Local Network"

    return "IP address only"


def session_dict(session):
    return {
        "id": session.id,
        "ip_address": session.ip_address,
        "location": location_from_ip(
            session.ip_address
        ),
        "device_type": session.device_type,
        "browser": session.browser,
        "operating_system": session.operating_system,
        "created_at": iso(session.created_at),
        "last_seen_at": iso(session.last_seen_at),
        "expires_at": iso(session.expires_at),
        "active": session.active
    }


def event_dict(event):
    return {
        "id": event.id,
        "session_id": event.session_id,
        "event_type": event.event_type,
        "ip_address": event.ip_address,
        "location": location_from_ip(
            event.ip_address
        ),
        "device_type": event.device_type,
        "browser": event.browser,
        "operating_system": event.operating_system,
        "created_at": iso(event.created_at)
    }


def risk_dict(risk):
    return {
        "id": risk.id,
        "session_id": risk.session_id,
        "classification": risk.classification,
        "ml_classification": risk.ml_classification,
        "risk_score": risk.risk_score,
        "anomaly_score": risk.anomaly_score,
        "ml_risk_score": risk.ml_risk_score,
        "action": risk.action,
        "created_at": iso(risk.created_at)
    }


def alert_dict(alert):
    return {
        "id": alert.id,
        "session_id": alert.session_id,
        "alert_type": alert.alert_type,
        "severity": alert.severity,
        "title": alert.title,
        "message": alert.message,
        "action": alert.action,
        "created_at": iso(alert.created_at),
        "resolved_at": iso(alert.resolved_at)
    }


def get_dashboard_data(user_id):

    sessions = (
        Session.query
        .filter_by(user_id=user_id)
        .all()
    )

    active_sessions = [
        session
        for session in sessions
        if session.active
    ]

    login_history = (
        SessionEvent.query
        .filter_by(user_id=user_id)
        .order_by(
            SessionEvent.created_at.desc()
        )
        .limit(50)
        .all()
    )

    risk_scores = (
        RiskAssessment.query
        .filter_by(user_id=user_id)
        .order_by(
            RiskAssessment.created_at.desc()
        )
        .limit(50)
        .all()
    )

    alerts = (
        SecurityAlert.query
        .filter_by(user_id=user_id)
        .order_by(
            SecurityAlert.created_at.desc()
        )
        .limit(50)
        .all()
    )

    blocked_attempts = [
        alert
        for alert in alerts
        if alert.action == "BLOCK"
    ]

    return {
        "active_sessions": [
            session_dict(s)
            for s in active_sessions
        ],

        "login_history": [
            event_dict(e)
            for e in login_history
        ],

        "risk_scores": [
            risk_dict(r)
            for r in risk_scores
        ],

        "blocked_attempts": [
            alert_dict(a)
            for a in blocked_attempts
        ],

        "security_alerts": [
            alert_dict(a)
            for a in alerts
        ],

        "counts": {
            "active_sessions":
                len(active_sessions),

            "login_history":
                len(login_history),

            "risk_scores":
                len(risk_scores),

            "blocked_attempts":
                len(blocked_attempts),

            "security_alerts":
                len(alerts)
        }
    }
