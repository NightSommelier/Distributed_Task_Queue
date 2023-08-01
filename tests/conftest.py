import random
import string
from collections import namedtuple, deque
from typing import NamedTuple

import pytest

from main import app as instance, tasks_queue, tasks_progress, Task


@pytest.fixture
def gen_string():
    return "".join(random.choices(string.digits + string.ascii_letters, k=30))


@pytest.fixture
def app():
    yield instance.test_client()


@pytest.fixture(name='tasks')
def queues():
    tasks = NamedTuple('Tasks', [('queue', deque[Task]), ('progress', list[Task])])
    yield tasks(queue=tasks_queue.queue, progress=tasks_progress)
