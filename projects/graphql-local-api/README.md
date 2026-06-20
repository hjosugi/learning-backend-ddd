# GraphQL Local API

Learn GraphQL request shape, resolver boundaries, and response contracts without a hosted
API key or framework dependency.

This is a deliberately small GraphQL-shaped lab. It is not a full GraphQL implementation;
use it to understand the moving parts before adding Apollo Server, GraphQL Yoga, Spring
for GraphQL, or federation tooling.

## Run

```bash
node projects/graphql-local-api/server.test.mjs
node projects/graphql-local-api/server.mjs
```

Example request:

```bash
curl -s http://127.0.0.1:8788/graphql \
  -H 'content-type: application/json' \
  -d '{"query":"{ books { id title author } }"}'
```

## What To Notice

- The HTTP endpoint is stable: `POST /graphql`.
- Resolvers decide which application data is exposed.
- Clients select fields, so backend code must handle partial responses deliberately.
- Validation, variables, introspection, batching, auth, and persisted queries are the next
  topics to add with a real GraphQL library.
