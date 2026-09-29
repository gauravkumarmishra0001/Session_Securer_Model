from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from app.services.session_service import (
    get_session_from_token,
    get_active_sessions_for_user,
    revoke_session,
    session_to_dict
)


sessions_bp = Blueprint(
    "sessions",
    __name__,
    url_prefix="/api/sessions"
)


def get_current_session():
    token = request.cookies.get(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    return get_session_from_token(
        token
    )


@sessions_bp.route(
    "",
    methods=["GET"]
)
def list_sessions():
    current_session = get_current_session()

    if current_session is None:
        return jsonify({
            "error": "authentication required"
        }), 401

    sessions = get_active_sessions_for_user(
        current_session.user_id
    )

    return jsonify({
        "sessions": [
            session_to_dict(session)
            for session in sessions
        ]
    }), 200


@sessions_bp.route(
    "/<int:session_id>",
    methods=["DELETE"]
)
def revoke_one_session(session_id):
    current_session = get_current_session()

    if current_session is None:
        return jsonify({
            "error": "authentication required"
        }), 401

    target = next(
        (
            session
            for session in current_session.user.sessions
            if session.id == session_id
        ),
        None
    )

    if target is None:
        return jsonify({
            "error": "session not found"
        }), 404

    if target.user_id != current_session.user_id:
        return jsonify({
            "error": "forbidden"
        }), 403

    revoke_session(target)

    return jsonify({
        "message": "session revoked",
        "session_id": session_id
    }), 200
