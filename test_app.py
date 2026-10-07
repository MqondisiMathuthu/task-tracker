import app as task_app

def test_home():
    client = task_app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Tracker is alive!" in response.get_json()["message"]

def test_add_task_requires_json_body():
    client = task_app.app.test_client()
    response = client.post("/tasks", json={})
    assert response.status_code == 400
