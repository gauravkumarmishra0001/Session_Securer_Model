
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    Response
)

from app.services.session_service import (
    get_session_from_token
)

from app.services.dashboard_service import (
    get_dashboard_data
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


def current_session():
    token = request.cookies.get(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    if not token:
        return None

    return get_session_from_token(token)


@dashboard_bp.route(
    "/api/dashboard/summary",
    methods=["GET"]
)
def summary():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    return jsonify(
        get_dashboard_data(
            session.user_id
        )
    ), 200


@dashboard_bp.route(
    "/api/dashboard/active-sessions",
    methods=["GET"]
)
def active_sessions():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "sessions":
            data["active_sessions"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/login-history",
    methods=["GET"]
)
def login_history():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "history":
            data["login_history"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/risk-scores",
    methods=["GET"]
)
def risk_scores():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "risk_scores":
            data["risk_scores"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/blocked-attempts",
    methods=["GET"]
)
def blocked_attempts():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "blocked_attempts":
            data["blocked_attempts"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/security-alerts",
    methods=["GET"]
)
def security_alerts():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "alerts":
            data["security_alerts"]
    }), 200


@dashboard_bp.route(
    "/dashboard",
    methods=["GET"]
)
