from main import app, tasks_progress

instance = app.test_client()


def test_main_mark_task_done_post() -> None:
    for task in tasks_progress:
        resp = instance.post(f'/tasks/{task.id}/complete')

        assert resp.status_code == 200
        assert '' in resp.get_data(as_text=True)


def test_main_mark_task_done_post_incorrect() -> None:
    for i in range(31, 41):
        resp = instance.post(f'/tasks/{i}/complete')

        assert resp.status_code == 404
