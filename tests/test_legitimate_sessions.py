import sys
from pathlib import Path
import uuid


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app import create_app


def test_multiple_legitimate_sessions():
    app = create_app()
    client = app.test_client()

    unique_id = uuid.uuid4().hex[:10]

    email = (
        f"legitimate_{unique_id}@example.com"
    )

    password = "LegitimatePassword123"

    register = client.post(
        "/api/auth/register",
        json={
            "username": f"legitimate_{unique_id}",
            "email": email,
            "password": password
        }
    )

    assert register.status_code == 201

    normal_agent = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Build normal history.
    for _ in range(5):
        login = client.post(
            "/api/auth/login",
            json={
                "email": email,
                "password": password
            },
            headers={
                "User-Agent": normal_agent
            }
        )

        assert login.status_code == 200

        detection = client.get(
            "/api/detection/current"
        )

        assert detection.status_code == 200

        data = detection.get_json()

        # First few sessions initialize the profile.
        # Later sessions should become normal.
        if data["classification"] != "INSUFFICIENT_HISTORY":
            assert data["classification"] == "NORMAL"
            assert data["anomaly_score"] == 0.0
