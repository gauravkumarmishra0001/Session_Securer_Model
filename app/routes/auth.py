from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from app.services.auth_service import (
    create_user,
    authenticate_user,
    normalize_email,
    create_session
)

from app.services.device_service import (
    get_device_info
)

from app.services.session_service import (
    get_session_from_token,
    update_last_seen,
    session_to_dict,
    revoke_session
)

from app.services.event_service import record_login_event


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


def user_to_dict(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():
    data = request.get_json(
        silent=True
    ) or {}

    username = str(
        data.get("username", "")
    ).strip()

    email = normalize_email(
        data.get("email", "")
    )

    password = data.get(
        "password",
        ""
    )

    if not username or not email or not password:
        return jsonify({
            "error": (
                "username, email and password "
                "are required"
            )
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": (
                "password must contain at least "
                "8 characters"
            )
        }), 400

    user = create_user(
        username,
        email,
        password
    )

    if user is None:
        return jsonify({
            "error": (
                "username or email already exists"
            )
        }), 409

    return jsonify({
        "message": "registration successful",
        "user": user_to_dict(user)
    }), 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():
    data = request.get_json(
        silent=True
    ) or {}

    email = normalize_email(
        data.get("email", "")
    )

    password = data.get(
        "password",
        ""
    )

    if not email or not password:
        return jsonify({
            "error": (
                "email and password are required"
            )
        }), 400

    user = authenticate_user(
        email,
        password
    )

    if user is None:
        return jsonify({
            "error": "invalid email or password"
        }), 401

    user_agent = request.headers.get(
        "User-Agent",
        ""
    )

    device_info = get_device_info(
        user_agent
    )

    raw_token, session = create_session(
        user=user,
        ip_address=request.remote_addr,
        user_agent=user_agent,
        device_info=device_info,
        ttl_seconds=current_app.config[
            "SESSION_TTL_SECONDS"
        ]
    )

    record_login_event(session)

    response = jsonify({
        "message": "login successful",
        "user": user_to_dict(user),
        "session": session_to_dict(session)
    })

    response.set_cookie(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ],
        raw_token,
        max_age=current_app.config[
            "SESSION_TTL_SECONDS"
        ],
        httponly=True,
        samesite="Strict",
        secure=current_app.config[
            "SESSION_COOKIE_SECURE"
        ]
    )

    return response, 200


@auth_bp.route(
    "/me",
    methods=["GET"]
)
def me():
    token = request.cookies.get(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    session = get_session_from_token(
        token
    )

    if session is None:
        return jsonify({
            "error": "authentication required"
        }), 401

    update_last_seen(session)

    return jsonify({
        "user": user_to_dict(
            session.user
        ),
        "session": session_to_dict(
            session
        )
    }), 200


@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():
    token = request.cookies.get(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    session = get_session_from_token(
        token
    )

    if session is not None:
        revoke_session(session)

    response = jsonify({
        "message": "logout successful"
    })

    response.delete_cookie(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    return response, 200
