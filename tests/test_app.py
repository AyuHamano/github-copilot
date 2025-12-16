from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Basic sanity: expected activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_participant():
    activity = "Tennis Club"
    email = "test_user@example.com"

    # Ensure user is not already present
    res = client.get("/activities")
    assert res.status_code == 200
    participants = res.json()[activity]["participants"]
    if email in participants:
        # Clean up if previous run left state
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Verify user now present
    res = client.get("/activities")
    assert res.status_code == 200
    participants = res.json()[activity]["participants"]
    assert email in participants

    # Unregister
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Verify removed
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email not in participants
