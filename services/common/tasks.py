import os

QUEUE_BACKEND = os.getenv("TASKS_BACKEND", "inproc")  # inproc|redis|none


def submit_task(name: str, payload: dict) -> dict:
    return {"taskId": "noop", "status": "done"}
