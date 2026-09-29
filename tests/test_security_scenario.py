import sys
from pathlib import Path
import uuid


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app import create_app


def test_new_device_generates_anomaly_signal():
    app = create_app()
    client = app.test_client()

    unique_id = uuid.uuid4().hex[:10]

    email = (
        f"security_{unique_id}@example.com"
    )

    password = "SecurityPassword123"

    register = client.post(
        "/api/auth/register",
        json={
            "username": f"security_{unique_id}",
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

    new_device_agent = (
        "Mozilla/5.0 "
        "(iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )

    # Establish normal behavior.
    for _ in range(3):
        response = client.post(
            "/api/auth/login",
            json={
                "email": email,
                "password": password
            },
            headers={
                "User-Agent": normal_agent
            }
        )

        assert response.status_code == 200

    # Simulate a new device.
    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password
        },
        headers={
            "User-Agent": new_device_agent
        }
    )

    assert response.status_code == 200

    detection = client.get(
        "/api/detection/current"
    )

    assert detection.status_code == 200

    result = detection.get_json()

    assert result["profile_status"] == "READY"

    assert result["features"]["new_device"] is True

    assert result["anomaly_score"] >= 0.30

    assert result["classification"] in (
        "UNUSUAL",
        "HIGH_ANOMALY"
    )
