from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from itertools import count
from typing import Any


@dataclass
class Task:
    id: int
    title: str
    status: str = "open"


class TaskRepository:
    def __init__(self) -> None:
        self._ids = count(1)
        self._tasks: dict[int, Task] = {}

    def create(self, title: str) -> Task:
        if len(title.strip()) < 3:
            raise ValueError("title must be at least 3 characters")
        task = Task(id=next(self._ids), title=title.strip())
        self._tasks[task.id] = task
        return task

    def list(self) -> list[Task]:
        return list(self._tasks.values())

    def complete(self, task_id: int) -> Task:
        task = self._tasks[task_id]
        task.status = "done"
        return task


repo = TaskRepository()
repo.create("Read the API contract")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.respond({"status": "ok"})
            return
        if self.path == "/tasks":
            self.respond([asdict(task) for task in repo.list()])
            return
        self.respond({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        if self.path != "/tasks":
            self.respond({"error": "not found"}, status=404)
            return
        try:
            payload = self.read_json()
            task = repo.create(str(payload.get("title", "")))
            self.respond(asdict(task), status=201)
        except ValueError as exc:
            self.respond({"error": str(exc)}, status=400)

    def do_PATCH(self) -> None:
        prefix = "/tasks/"
        suffix = "/complete"
        if not (self.path.startswith(prefix) and self.path.endswith(suffix)):
            self.respond({"error": "not found"}, status=404)
            return
        try:
            task_id = int(self.path.removeprefix(prefix).removesuffix(suffix))
            self.respond(asdict(repo.complete(task_id)))
        except (KeyError, ValueError):
            self.respond({"error": "task not found"}, status=404)

    def read_json(self) -> dict[str, Any]:
        size = int(self.headers.get("content-length", "0"))
        if size == 0:
            return {}
        return json.loads(self.rfile.read(size))

    def respond(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def demo() -> None:
    local = TaskRepository()
    task = local.create("Model one use case")
    local.complete(task.id)
    print(json.dumps([asdict(item) for item in local.list()], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        demo()
        return
    server = ThreadingHTTPServer(("127.0.0.1", 8080), Handler)
    print("listening on http://127.0.0.1:8080")
    server.serve_forever()


if __name__ == "__main__":
    main()

