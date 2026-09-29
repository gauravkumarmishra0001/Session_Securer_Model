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


def test_application_creation():
    app = create_app()
    assert app is not None


def test_registration():
    client = create_test_client()

    unique_id = uuid.uuid4().hex[:10]

    response = client.post(
        "/api/auth/register",
        json={
            "username": f"testuser_{unique_id}",
            "email": f"test_{unique_id}@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 201


def test_invalid_login():
    client = create_test_client()

    response = client.post(
        "/api/auth/login",
        json={
            "email": "doesnotexist@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401


def test_full_authentication_flow():
    client = create_test_client()

    unique_id = uuid.uuid4().hex[:10]

    username = f"flowuser_{unique_id}"
    email = f"flow_{unique_id}@example.com"
    password = "FlowPassword123"

    register_response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert login_response.status_code == 200

    me_response = client.get(
        "/api/auth/me"
    )

    assert me_response.status_code == 200

    sessions_response = client.get(
        "/api/sessions"
    )

    assert sessions_response.status_code == 200

    sessions = sessions_response.get_json()["sessions"]

    assert len(sessions) >= 1

    logout_response = client.post(
        "/api/auth/logout"
    )

    assert logout_response.status_code == 200

    after_logout_response = client.get(
        "/api/auth/me"
    )

    assert after_logout_response.status_code == 401
