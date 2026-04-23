"""
Test suite for FastAPI activities endpoints using TestClient
"""

from fastapi.testclient import TestClient
from src.app import app

# Create a TestClient instance
client = TestClient(app)


class TestActivities:
    """Test cases for activities endpoints"""

    def test_get_activities(self):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert "Chess Club" in response.json()

    def test_get_activities_structure(self):
        """Test that activities have required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_signup_for_activity(self):
        """Test signing up for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_duplicate_student(self):
        """Test that duplicate signups are rejected"""
        email = "duplicate@mergington.edu"
        # First signup
        client.post("/activities/Chess Club/signup", params={"email": email})
        # Attempt duplicate signup
        response = client.post("/activities/Chess Club/signup", params={"email": email})
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self):
        """Test signing up for a non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_participant(self):
        """Test removing a participant from an activity"""
        email = "remove@mergington.edu"
        # First, sign up
        client.post("/activities/Gym Class/signup", params={"email": email})
        # Then, remove
        response = client.delete(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]

    def test_remove_nonexistent_participant(self):
        """Test removing a participant who isn't in the activity"""
        response = client.delete(
            "/activities/Programming Class/signup",
            params={"email": "notinactivity@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_from_nonexistent_activity(self):
        """Test removing from a non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]