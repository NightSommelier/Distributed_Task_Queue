### Problem Statement: "Distributed Task Queue"

**Background:**

A distributed task queue is a core component of many high-load systems. In essence, a task queue is a simple tool: clients put tasks in a queue, and workers take tasks from the queue and execute them.

**Your Task:**

Design and implement a simple REST API for a task queue in Python using Flask. For simplicity, we will consider only two types of clients: producers and consumers. Producers add tasks to the queue, and consumers retrieve tasks from the queue for processing. Tasks are represented as simple strings.

Your Flask application should implement the following endpoints:

1. `POST /tasks/`: This endpoint is used by producers to add a new task to the queue. The task data is sent in the request body as JSON, for example: `{"task": "Task description"}`. If the task is added successfully, the endpoint should return HTTP status 201 and the task ID as JSON, for example: `{"id": 1}`.

2. `GET /tasks/`: This endpoint is used by consumers to retrieve a task from the queue. The server should return the oldest task that isn't currently being processed. The task should be returned as JSON, for example: `{"id": 1, "task": "Task description"}`. If there are no available tasks, the server should return an appropriate HTTP status code.

3. `POST /tasks/<id>/complete`: This endpoint is used by consumers to indicate that they have completed a task. If the task is marked as completed successfully, the server should return HTTP status 200 and an empty body. If the task with the given ID doesn't exist or wasn't being processed, the server should return an appropriate HTTP status code.

You can use any data storage method you prefer: in-memory data structures, a database, etc.

**Constraints:**

- The task ID is a unique integer assigned by the server. The first task has the ID 1, the second task has the ID 2, and so on.
- Each task can be processed by only one consumer at a time. When a consumer retrieves a task from the queue, the task shouldn't be given to any other consumer until it's either completed or released back into the queue.
- The task queue should be thread-safe, i.e., it should support concurrent requests from multiple producers and consumers.
