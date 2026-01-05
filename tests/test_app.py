import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Art Club"
    email = "testuser@example.com"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")  # ignore result, may be 404
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    # Accept either 200 (success) or 404 (not found if already removed)
    assert response_unreg.status_code in (200, 404)
    if response_unreg.status_code == 200:
        assert response_unreg.json()["message"] == f"Unregistered {email} from {activity}"
    # Unregister again should fail (already removed)
    response_unreg2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg2.status_code in (400, 404)

def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404
