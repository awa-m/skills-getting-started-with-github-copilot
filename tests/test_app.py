def test_unregister_from_activity_success():
    email = "testuser3@example.com"
    # まず登録
    client.post(f"/activities/Drama Society/signup?email={email}")
    # 登録解除
    response = client.delete(f"/activities/Drama Society/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from Drama Society" in response.json()["message"]

def test_unregister_from_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister?email=someone@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_participant_not_found():
    response = client.delete("/activities/Math Olympiad/unregister?email=notfound@example.com")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# 各テスト前にactivitiesを初期状態にリセット
@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy({
        "Basketball Team": {
            "description": "Join the school basketball team for training and competitions",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": []
        },
        "Soccer Club": {
            "description": "Participate in soccer practice and matches",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 18,
            "participants": []
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": []
        },
        "Drama Society": {
            "description": "Act, direct, and produce school plays and performances",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": []
        },
        "Math Olympiad": {
            "description": "Prepare for and compete in mathematics competitions",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": []
        },
        "Debate Club": {
            "description": "Practice public speaking and participate in debates",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": []
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    })
    activities.clear()
    activities.update(copy.deepcopy(original))

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
