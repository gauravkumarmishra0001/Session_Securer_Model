
import secrets
from datetime import timedelta

from app.database import db
from app.models.otp_challenge import (
    OTPChallenge,
    utc_now
)


PREVENTION_MIN_HISTORY = 3
OTP_EXPIRY_SECONDS = 300


def determine_prevention_action(result):
    """
    Convert detection output into a prevention decision.

    NORMAL / insufficient history:
        ALLOW

    Both rule and ML classify as UNUSUAL:
        VERIFY

    Both rule and ML classify as HIGH_RISK:
        BLOCK
    """

    if result is None:
        return "ALLOW"

    profile_status = result.get(
        "profile_status"
    )

    historical_events = int(
        result.get("historical_events", 0) or 0
    )

    classification = result.get(
        "classification",
        "NORMAL"
    )

    ml_classification = result.get(
        "ml_classification",
        "MODEL_UNAVAILABLE"
    )

    if profile_status == "INITIALIZING":
        return "ALLOW"

    if classification == "INSUFFICIENT_HISTORY":
        return "ALLOW"

    if historical_events < PREVENTION_MIN_HISTORY:
        return "ALLOW"

    # Normal rule-based result should never be blocked.
    if classification == "NORMAL":
        return "ALLOW"

    # Require agreement between both detection layers.
    if (
        classification == "HIGH_RISK"
        and ml_classification == "HIGH_RISK"
    ):
        return "BLOCK"

    if (
        classification == "UNUSUAL"
        and ml_classification == "UNUSUAL"
    ):
        return "VERIFY"

    return "ALLOW"


def create_otp_challenge(session):
    """
    Create a short-lived OTP challenge.

    The OTP itself is never stored.
    Only its SHA-256 hash is stored.
    """

    # Invalidate any previous active challenge.
    old_challenges = OTPChallenge.query.filter_by(
        session_id=session.id,
        used_at=None
    ).all()

    for challenge in old_challenges:
        challenge.mark_used()

    otp = f"{secrets.randbelow(1000000):06d}"

    challenge = OTPChallenge(
        user_id=session.user_id,
        session_id=session.id,
        otp_hash=OTPChallenge.hash_otp(otp),
        created_at=utc_now(),
        expires_at=utc_now() + timedelta(
            seconds=OTP_EXPIRY_SECONDS
        )
    )

    db.session.add(challenge)
    db.session.commit()

    return challenge, otp


def verify_otp(challenge, otp):
    if challenge is None:
        return False

    if not challenge.active:
        return False

    if OTPChallenge.hash_otp(otp) != challenge.otp_hash:
        return False

    challenge.mark_used()
    db.session.commit()

    return True


def revoke_suspicious_session(session):
    if session is None:
        return

    from app.services.session_service import revoke_session

    revoke_session(session)
