import random


def test_tasks_post(app, gen_string) -> None:
    for _ in range(20):
        resp = app.post("/tasks/", json=dict(
            task=gen_string
        ))
        json: dict = resp.get_json()

        assert resp.status_code == 201
        assert 'id' in json.keys()
        assert isinstance(json.get('id'), int)


def test_tasks_post_incorrect(app) -> None:
    resp = app.post('/tasks/', json=dict(
        task=random.randint(1, 5_000)
    ))

    assert resp.status_code == 400
    assert 'Error type task' in resp.get_data(as_text=True)


def test_tasks_post_incorrect_body(app) -> None:
    resp = app.post('/tasks/', json=dict(
        name="First task",
        quentity=1.1
    ))

    assert resp.status_code == 400
    assert 'Error key task' in resp.get_data(as_text=True)
