import sys
from pathlib import Path
import uuid


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app import create_app


def create_test_client():
    app = create_app()
    return app.test_client()


def register_user(client):
    unique_id = uuid.uuid4().hex[:10]

    username = f"phase2_{unique_id}"
    email = f"phase2_{unique_id}@example.com"
    password = "Phase2Password123"

    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 201

    return email, password


def login_user(
    client,
    email,
    password,
    user_agent
):
    return client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password
        },
        headers={
            "User-Agent": user_agent
        }
    )


def test_detection_requires_login():
    client = create_test_client()

    response = client.get(
        "/api/detection/current"
    )

    assert response.status_code == 401


def test_detection_initializing():
    client = create_test_client()

    email, password = register_user(client)

    response = login_user(
        client,
        email,
        password,
        "Mozilla/5.0 Windows Chrome"
    )

    assert response.status_code == 200

    detection = client.get(
        "/api/detection/current"
    )

    assert detection.status_code == 200

    data = detection.get_json()

    assert data["classification"] == (
        "INSUFFICIENT_HISTORY"
    )


def test_detection_normal_after_history():
    client = create_test_client()

    email, password = register_user(client)

    user_agent = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    for _ in range(3):
        response = login_user(
            client,
            email,
            password,
            user_agent
        )

        assert response.status_code == 200

    response = login_user(
        client,
        email,
        password,
        user_agent
    )

    assert response.status_code == 200

    detection = client.get(
        "/api/detection/current"
    )

    assert detection.status_code == 200

    data = detection.get_json()

    assert data["profile_status"] == "READY"
    assert data["historical_events"] >= 3
    assert data["classification"] == "NORMAL"
    assert data["anomaly_score"] == 0.0


def test_detection_unusual_device():
    client = create_test_client()

    email, password = register_user(client)

    normal_user_agent = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    unusual_user_agent = (
        "Mozilla/5.0 "
        "(iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )

    for _ in range(3):
        response = login_user(
            client,
            email,
            password,
            normal_user_agent
        )

        assert response.status_code == 200

    response = login_user(
        client,
        email,
        password,
        unusual_user_agent
    )

    assert response.status_code == 200

    detection = client.get(
        "/api/detection/current"
    )

    assert detection.status_code == 200

    data = detection.get_json()

    assert data["profile_status"] == "READY"

    assert data["features"]["new_device"] is True

    assert data["classification"] in (
        "UNUSUAL",
        "HIGH_ANOMALY"
    )

    assert data["anomaly_score"] >= 0.30
