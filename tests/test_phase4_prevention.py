
import sys
import uuid
from unittest.mock import patch

from app import create_app


def make_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


def unique_user(prefix):
    uid = uuid.uuid4().hex[:12]
    return f"{prefix}_{uid}", f"{prefix}_{uid}@example.com"


def register_user(client, username, email):
    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201, (
        f"Registration failed: "
        f"{response.status_code} {response.get_json()}"
    )

    return response


def normal_result():
    return {
        "classification": "NORMAL",
        "ml_classification": "NORMAL",
        "ml_available": True,
        "historical_events": 10,
        "profile_status": "READY",
        "risk_score": 0.05
    }


def unusual_result():
    return {
        "classification": "UNUSUAL",
        "ml_classification": "UNUSUAL",
        "ml_available": True,
        "historical_events": 10,
        "profile_status": "READY",
        "risk_score": 0.65
    }


def high_risk_result():
    return {
        "classification": "HIGH_RISK",
        "ml_classification": "HIGH_RISK",
        "ml_available": True,
        "historical_events": 10,
        "profile_status": "READY",
        "risk_score": 0.95
    }


def patch_all_analyze_session_functions(result):
    """
    Patch every loaded app module that exposes analyze_session.

    This avoids assuming that auth.py directly imports analyze_session.
    """
    patches = []

    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("app."):
            continue

        if hasattr(module, "analyze_session"):
            try:
                patcher = patch.object(
                    module,
                    "analyze_session",
                    return_value=result
                )
                patcher.start()
                patches.append(patcher)
            except Exception:
                pass

    return patches


def stop_patches(patches):
    for patcher in patches:
        try:
            patcher.stop()
        except Exception:
            pass


def test_normal_login_allowed():
    app = make_app()

    with app.app_context():
        client = app.test_client()

        username, email = unique_user("p4_normal")
        register_user(client, username, email)

        patches = patch_all_analyze_session_functions(normal_result())

        try:
            response = client.post(
                "/api/auth/login",
                json={
                    "email": email,
                    "password": "StrongPass123"
                }
            )
        finally:
            stop_patches(patches)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: "
            f"{response.get_json()}"
        )


def test_unusual_login_requires_otp():
    app = make_app()

    with app.app_context():
        client = app.test_client()

        username, email = unique_user("p4_unusual")
        register_user(client, username, email)

        patches = patch_all_analyze_session_functions(
            unusual_result()
        )

        try:
            response = client.post(
                "/api/auth/login",
                json={
                    "email": email,
                    "password": "StrongPass123"
                }
            )
        finally:
            stop_patches(patches)

        assert response.status_code == 202, (
            f"Expected 202, got {response.status_code}: "
            f"{response.get_json()}"
        )


def test_high_risk_login_blocked():
    app = make_app()

    with app.app_context():
        client = app.test_client()

        username, email = unique_user("p4_block")
        register_user(client, username, email)

        patches = patch_all_analyze_session_functions(
            high_risk_result()
        )

        try:
            response = client.post(
                "/api/auth/login",
                json={
                    "email": email,
                    "password": "StrongPass123"
                }
            )
        finally:
            stop_patches(patches)

        assert response.status_code == 403, (
            f"Expected 403, got {response.status_code}: "
            f"{response.get_json()}"
        )


def test_invalid_otp_rejected():
    app = make_app()

    with app.app_context():
        client = app.test_client()

        username, email = unique_user("p4_invalid")
        register_user(client, username, email)

        patches = patch_all_analyze_session_functions(
            unusual_result()
        )

        try:
            response = client.post(
                "/api/auth/login",
                json={
                    "email": email,
                    "password": "StrongPass123"
                }
            )
        finally:
            stop_patches(patches)

        assert response.status_code == 202, (
            f"Expected 202, got {response.status_code}: "
            f"{response.get_json()}"
        )

        data = response.get_json() or {}

        session_id = (
            data.get("session_id")
            or data.get("id")
            or (data.get("session") or {}).get("id")
        )

        otp_id = (
            data.get("otp_id")
            or data.get("challenge_id")
            or data.get("otp_challenge_id")
        )

        payload = {
            "otp": "000000"
        }

        if session_id is not None:
            payload["session_id"] = session_id

        if otp_id is not None:
            payload["otp_id"] = otp_id

        verify = client.post(
            "/api/prevention/otp/verify",
            json=payload
        )

        assert verify.status_code == 403, (
            f"Expected invalid OTP to return 403, "
            f"got {verify.status_code}: {verify.get_json()}"
        )


def test_otp_single_use():
    app = make_app()

    with app.app_context():
        client = app.test_client()

        username, email = unique_user("p4_replay")
        register_user(client, username, email)

        patches = patch_all_analyze_session_functions(
            unusual_result()
        )

        try:
            response = client.post(
                "/api/auth/login",
                json={
                    "email": email,
                    "password": "StrongPass123"
                }
            )
        finally:
            stop_patches(patches)

        assert response.status_code == 202, (
            f"Expected 202, got {response.status_code}: "
            f"{response.get_json()}"
        )

        data = response.get_json() or {}

        session_id = (
            data.get("session_id")
            or data.get("id")
            or (data.get("session") or {}).get("id")
        )

        otp_id = (
            data.get("otp_id")
            or data.get("challenge_id")
            or data.get("otp_challenge_id")
        )

        otp = data.get("otp") or data.get("code")

        assert session_id is not None or otp_id is not None, (
            f"No session/OTP identifier returned: {data}"
        )

        verify_payload = {
            "otp": otp or "123456"
        }

        if session_id is not None:
            verify_payload["session_id"] = session_id

        if otp_id is not None:
            verify_payload["otp_id"] = otp_id

        first = client.post(
            "/api/prevention/otp/verify",
            json=verify_payload
        )

        assert first.status_code in (200, 201), (
            f"First OTP verification failed: "
            f"{first.status_code} {first.get_json()}"
        )

        second = client.post(
            "/api/prevention/otp/verify",
            json=verify_payload
        )

        assert second.status_code == 403, (
            f"OTP replay should be rejected. "
            f"Got {second.status_code}: {second.get_json()}"
        )
