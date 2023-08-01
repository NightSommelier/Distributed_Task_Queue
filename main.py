import queue
from threading import BoundedSemaphore
from typing import NamedTuple

from flask import Flask, request
from flask_restful import Resource, Api

# Init
app = Flask(__name__)
api = Api(app)

# Dynamic ID for tasks
_INDEX = 1
# Max connections for threads
_MAX_CONNECTION = 4

tasks_queue = queue.Queue()
tasks_progress = []
pool = BoundedSemaphore(value=_MAX_CONNECTION)


def get_index():
    global _INDEX
    with pool:
        idx = _INDEX
        _INDEX += 1
    return idx


class Task(NamedTuple):
    id: int
    task: str


class Tasks(Resource):
    def post(self):  # noqa
        data = request.get_json()

        if 'task' not in data.keys():
            return 'Error key task', 400

        if not isinstance(data['task'], str):
            return 'Error type task', 400

        idx = get_index()
        task = Task(id=idx, task=data['task'])

        tasks_queue.put(task, block=False)
        return {'id': idx}, 201

    def get(self):  # noqa
        try:
            task = tasks_queue.get(block=False)
            with pool:
                tasks_progress.append(task)
                return {'id': task.id, 'task': task.task}, 200
        except queue.Empty:
            return 'Task queue is empty', 404


class MarkTaskDone(Resource):
    def post(self, task_id: int):  # noqa
        with pool:
            for i, task in enumerate(tasks_progress):
                if task.id == task_id:
                    del tasks_progress[i]
                    return '', 200

        return 'Not found', 404


api.add_resource(Tasks, '/tasks/')
api.add_resource(MarkTaskDone, '/tasks/<int:task_id>/complete')

if __name__ == '__main__':
    app.run(debug=True)  # pragma: no cover
