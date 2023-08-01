from main import app

instance = app.test_client()


def test_tasks_get():
    for _ in range(20):
        resp = instance.get('/tasks/')
        json: dict = resp.get_json()

        assert resp.status_code == 200
        assert 'id' in json.keys()
        assert 'task' in json.keys()
        assert isinstance(json.get('id'), int)
        assert isinstance(json.get('task'), str)


def test_tasks_get_empty() -> None:
    resp = instance.get('/tasks/')

    assert resp.status_code == 404
    assert 'Task queue is empty' in resp.get_data(as_text=True)
