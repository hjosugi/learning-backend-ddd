# Go HTTP API

Runnable Go backend slice for request routing, JSON contracts, validation, and unit tests.

## Run

```bash
cd projects/go-http-api
go run .
```

Then call:

```bash
curl http://localhost:8081/healthz
curl http://localhost:8081/tasks
curl -X POST http://localhost:8081/tasks -d '{"title":"learn Go handlers"}'
```

## Test

```bash
cd projects/go-http-api
go test ./...
```

## What To Learn

- `net/http` handler boundaries
- JSON request/response contracts
- validation before domain mutation
- table tests around behavior

