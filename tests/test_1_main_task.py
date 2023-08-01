import random

from main import Task


def test_task(gen_string):
    task = Task(
        id=random.randint(0, 1_000),
        task=gen_string
    )

    assert isinstance(task.id, int)
    assert isinstance(task.task, str)
    assert len(task.task) == 30
