import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "participants" in data["Basketball Team"]

def test_signup_for_activity_success():
    email = "testuser1@example.com"
    response = client.post(f"/activities/Basketball Team/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for Basketball Team" in response.json()["message"]
    # Clean up for idempotency
    data = client.get("/activities").json()
    data["Basketball Team"]["participants"].remove(email)

def test_signup_for_activity_already_signed_up():
    email = "testuser2@example.com"
    # First signup
    client.post(f"/activities/Soccer Club/signup?email={email}")
    # Try to sign up for another activity
    response = client.post(f"/activities/Art Club/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    data = client.get("/activities").json()
    data["Soccer Club"]["participants"].remove(email)

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
