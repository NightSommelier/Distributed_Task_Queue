import queue
import random
import string
from queue import Queue
from threading import Thread, current_thread, BoundedSemaphore
from time import sleep

from main import Task


def test_multithread_post_and_get(app, tasks, gen_string) -> None:
    _producer_cycles = random.randint(20, 50)
    _consumer_cycles = random.randint(15, 100)
    _result = Queue()

    print()

    def producer_post():
        resp = app.post('/tasks/', json=dict(
            task="".join(random.choices(string.digits + string.ascii_letters, k=30))
        ))
        prod_name = current_thread().name

        print(f'{prod_name} post {resp.status_code}')
        assert resp.status_code == 201

    def consumer_get():
        resp = app.get('/tasks/')
        json = resp.get_json()

        cons_name = current_thread().name

        print(f'{cons_name} get {resp.status_code}')
        assert resp.status_code in [200, 404]

        if resp.status_code == 200:
            _result.put(json, block=False)

    threads = []

    for i in range(_producer_cycles):
        thr = Thread(target=producer_post, name=f'Producer {i}')
        threads.append(thr)

    for i in range(_consumer_cycles):
        thr = Thread(target=consumer_get, name=f'Consumer {i}')
        threads.append(thr)

    random.shuffle(threads)

    for i, thr in enumerate(threads):
        thr.start()

        if i % 2 == 0:
            sleep(random.uniform(.05, .3))

    # max threads working
    pool = BoundedSemaphore(value=3)

    def task_done():
        with pool:
            task: Task = Task(**_result.get(block=False))
            print(f"[{current_thread().name}] working with {task=}")
            resp = app.post(f'/tasks/{task.id}/complete')

            assert resp.status_code == 200

    while list(_result.queue):
        try:
            Thread(target=task_done).start()
        except queue.Empty:
            break

