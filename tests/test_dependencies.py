from datetime import datetime, timedelta, timezone

from jose import jwt 

from task_tracker_api.config import settings
from task_tracker_api.security import ALGORITHM

def test_access_protected_route_without_token(client):
    # Tidak ada header Authorization
    response = client.get("/tasks/")

    assert response.status_code == 401 
    assert response.json()["detail"] == "Not authenticated"

def test_access_protected_route_with_invalid_token(client):
    response = client.get(
        "/tasks/",
        headers={
            "Authorization": "Bearer ini-token-palsu-random",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_access_protected_route_with_expired_token(client):
    # Token yang sudah expired
    expired_payload = {
        "sub": "someone@example.com",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
    }

    expired_token = jwt.encode(
        expired_payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {expired_token}",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"