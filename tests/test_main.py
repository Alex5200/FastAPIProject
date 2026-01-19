from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_chatmessage():
    response = client.post(
        "/chatmessage/",
        json={"name": "Test Chatmessage", "description": "A chatmessage for testing"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Chatmessage"


def test_read_chatmessage():
    response = client.post(
        "/chatmessage/",
        json={"name": "Test Chatmessage", "description": "A chatmessage for testing"},
    )
    item_id = response.json()["id"]
    response = client.get(f"/chatmessage/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Chatmessage"


def test_update_chatmessage():
    response = client.post(
        "/chatmessage/",
        json={"name": "Test Chatmessage", "description": "A chatmessage for testing"},
    )
    item_id = response.json()["id"]
    response = client.put(
        f"/chatmessage/{item_id}",
        json={"name": "Updated Chatmessage", "description": "Updated description"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Chatmessage"


def test_delete_chatmessage():
    response = client.post(
        "/chatmessage/",
        json={"name": "Test Chatmessage", "description": "A chatmessage for testing"},
    )
    item_id = response.json()["id"]
    response = client.delete(f"/chatmessage/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Chatmessage"
