import app as task_app

def test_home():
    client = task_app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task Tracker is alive!"

def test_add_task_requires_json_body():
    client = task_app.app.test_client()
    response = client.post("/tasks", json={})
    assert response.status_code == 400
