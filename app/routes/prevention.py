
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request
)

from app.database import db
from app.models.otp_challenge import OTPChallenge
from app.models.session import Session
from app.services.prevention_service import (
    verify_otp
)
from app.services.session_service import (
    session_to_dict
)


prevention_bp = Blueprint(
    "prevention",
    __name__,
    url_prefix="/api/prevention"
)


@prevention_bp.route(
    "/otp/verify",
    methods=["POST"]
)
def verify_otp_route():

    data = request.get_json(
        silent=True
    ) or {}

    otp = str(
        data.get("otp", "")
    ).strip()

    session_id = data.get(
        "session_id"
    )

    otp_id = data.get(
        "otp_id"
    )

    if not otp:
        return jsonify({
            "error": "OTP is required"
        }), 400

    challenge = None

    if otp_id is not None:
        try:
            challenge = OTPChallenge.query.get(
                int(otp_id)
            )
        except (TypeError, ValueError):
            challenge = None

    if challenge is None and session_id is not None:
        try:
            challenge = (
                OTPChallenge.query
                .filter_by(
                    session_id=int(session_id),
                    used_at=None
                )
                .order_by(
                    OTPChallenge.id.desc()
                )
                .first()
            )
        except (TypeError, ValueError):
            challenge = None

    if challenge is None:
        return jsonify({
            "error": "OTP challenge not found"
        }), 403

    if not verify_otp(
        challenge,
        otp
    ):
        return jsonify({
            "error": "invalid or expired OTP"
        }), 403

    session = Session.query.get(
        challenge.session_id
    )

    if session is None:
        return jsonify({
            "error": "session not found"
        }), 404

    # The session was kept inactive while waiting
    # for OTP verification. Activate it now.
    session.revoked_at = None
    db.session.commit()

    response = jsonify({
        "message": "OTP verification successful",
        "session": session_to_dict(session)
    })

    return response, 200
