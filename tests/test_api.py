from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_activity_and_duplicate_rejection():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Act (duplicate signup)
    response_dup = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"].lower()


def test_remove_participant():
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity_name}" in response.json()["message"]

    # Verify removal
    response_check = client.get("/activities")
    assert response_check.status_code == 200
    participants = response_check.json()[activity_name]["participants"]
    assert email not in participants


def test_remove_nonexistent_participant():
    # Arrange
    activity_name = "Gym Class"
    email = "doesnotexist@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
