# Task API Stdlib

A tiny backend project that shows request handling, domain functions, and JSON responses without framework setup.

## Run A Demo

```bash
python3 projects/task-api-stdlib/app.py --demo
```

## Run The Server

```bash
python3 projects/task-api-stdlib/app.py
```

Then call:

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/tasks
curl -X POST http://localhost:8080/tasks -d '{"title":"Write validation test"}'
```

## Test Domain Logic

```bash
python3 projects/task-api-stdlib/test_domain.py
```

