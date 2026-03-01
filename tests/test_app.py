"""Unit/integration tests for Task API - run in CI."""
import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_create_task(client):
    r = client.post("/tasks", json={"title": "Test", "description": "D"})
    assert r.status_code == 201
    data = r.get_json()
    assert "id" in data and data["title"] == "Test" and data["description"] == "D"


def test_create_task_requires_title(client):
    r = client.post("/tasks", json={"description": "Only desc"})
    assert r.status_code == 400


def test_list_tasks(client):
    client.post("/tasks", json={"title": "A", "description": ""})
    r = client.get("/tasks")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


def test_get_task_by_id(client):
    cr = client.post("/tasks", json={"title": "One", "description": "Desc"})
    tid = cr.get_json()["id"]
    r = client.get(f"/tasks/{tid}")
    assert r.status_code == 200
    assert r.get_json()["title"] == "One"


def test_get_task_404(client):
    r = client.get("/tasks/nonexistent-id")
    assert r.status_code == 404


def test_update_task(client):
    cr = client.post("/tasks", json={"title": "Old", "description": "D"})
    tid = cr.get_json()["id"]
    r = client.put(f"/tasks/{tid}", json={"title": "New", "status": "done"})
    assert r.status_code == 200
    assert r.get_json()["title"] == "New" and r.get_json()["status"] == "done"


def test_update_task_404(client):
    r = client.put("/tasks/nonexistent-id", json={"title": "X"})
    assert r.status_code == 404


def test_delete_task(client):
    cr = client.post("/tasks", json={"title": "To delete", "description": ""})
    tid = cr.get_json()["id"]
    r = client.delete(f"/tasks/{tid}")
    assert r.status_code == 204
    assert client.get(f"/tasks/{tid}").status_code == 404


def test_delete_task_404(client):
    r = client.delete("/tasks/nonexistent-id")
    assert r.status_code == 404
