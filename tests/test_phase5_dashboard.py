
import uuid

from app import create_app
from app.database import db

from app.models.risk_assessment import RiskAssessment
from app.models.security_alert import SecurityAlert


def make_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


def unique_user():
    uid = uuid.uuid4().hex[:12]

    return (
        "dashboard_" + uid,
        "dashboard_" + uid + "@example.com"
    )


def register_and_login(client):

    username, email = unique_user()

    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200

    return response


def test_dashboard_requires_login():

    app = make_app()
    client = app.test_client()

    response = client.get(
        "/api/dashboard/summary"
    )

    assert response.status_code == 401


def test_dashboard_summary():

    app = make_app()
    client = app.test_client()

    register_and_login(client)

    response = client.get(
        "/api/dashboard/summary"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "active_sessions" in data
    assert "login_history" in data
    assert "risk_scores" in data
    assert "blocked_attempts" in data
    assert "security_alerts" in data
    assert "counts" in data

    assert data["counts"]["active_sessions"] >= 1
    assert data["counts"]["login_history"] >= 1


def test_dashboard_page():

    app = make_app()
    client = app.test_client()

    register_and_login(client)

    response = client.get(
        "/dashboard"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        "Session Securer Security Dashboard"
        in html
    )

    assert "Active Sessions" in html
    assert "Login History" in html
    assert "Risk Scores" in html
    assert "Blocked Attempts" in html
    assert "Security Alerts" in html


def test_dashboard_risk_and_alert_data():

    app = make_app()
    client = app.test_client()

    register_and_login(client)

    with app.app_context():

        from app.models.session import Session

        session = (
            Session.query
            .order_by(
                Session.id.desc()
            )
            .first()
        )

        risk = RiskAssessment(
            user_id=session.user_id,
            session_id=session.id,
            classification="UNUSUAL",
            ml_classification="UNUSUAL",
            risk_score=0.65,
            anomaly_score=0.65,
            ml_risk_score=0.65,
            action="VERIFY"
        )

        alert = SecurityAlert(
            user_id=session.user_id,
            session_id=session.id,
            alert_type="LOGIN_RISK",
            severity="MEDIUM",
            title="Suspicious login activity",
            message="Verification required",
            action="VERIFY"
        )

        db.session.add(risk)
        db.session.add(alert)

        db.session.commit()

    response = client.get(
        "/api/dashboard/summary"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(
        data["risk_scores"]
    ) >= 1

    assert len(
        data["security_alerts"]
    ) >= 1
