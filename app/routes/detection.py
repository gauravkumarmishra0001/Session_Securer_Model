from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from app.services.session_service import (
    get_session_from_token
)

from app.services.detection_service import (
    analyze_session
)


detection_bp = Blueprint(
    "detection",
    __name__,
    url_prefix="/api/detection"
)


@detection_bp.route(
    "/current",
    methods=["GET"]
)
def current_detection():
    """
    Analyze the currently authenticated session.
    """

    token = request.cookies.get(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    session = get_session_from_token(token)

    if session is None:
        return jsonify({
            "error": "authentication required"
        }), 401

    result = analyze_session(session)

    return jsonify(result), 200
