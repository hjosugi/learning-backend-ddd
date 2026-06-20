# Learning Backend DDD

Backend and DDD learning path across Spring Boot, Quarkus, Go/Gin, Phoenix, TypeScript service patterns, and local development services.

Last verified: 2026-06-20

## Baseline

- Java 21 as local default, Java 25 LTS as target where available
- Spring Boot 4.1.0 for new Spring examples
- Go 1.26.x
- PostgreSQL-oriented persistence examples
- OpenAPI/request-response examples where useful

## What This Repo Teaches

This repo is for backend system design through small runnable services.

The examples should make these concerns visible:

- request/response contracts and validation errors
- transaction boundaries and persistence tradeoffs
- where DDD vocabulary clarifies the code and where it adds ceremony
- local dependency strategy for integration tests
- framework differences between Spring Boot, Quarkus, Go/Gin, Phoenix, and TypeScript service code
- operational hooks such as health checks, metrics, and structured logs

## Source Repositories

- `flux-sample`
- `tasklist`
- `ddd-spring-boot`
- `quarkus-ddd`
- `gin-sample`
- `realworld-phx`
- `ts-ddd`
- `java-sandbox`
- `local-mail-api`

## Learning Path

1. REST API basics
2. validation and error responses
3. persistence and transactions
4. DDD vocabulary
5. Spring MVC/JPA
6. WebFlux/R2DBC
7. Quarkus
8. Go/Gin
9. Phoenix architecture reading
10. local development services such as GreenMail

## Planned Structure

```text
apps/
  spring-tasklist/
  spring-ddd/
  spring-webflux-r2dbc/
  quarkus-ddd/
  gin-api/
  local-mail-api/
reading/
  phoenix-realworld/
docs/
  2026-learning-items.md
  ddd-vocabulary.md
  framework-comparison.md
  repository-profile.md
```

## Study Loop

1. start with one use case and write the API contract
2. implement it in one framework
3. add validation, persistence, and a testable local dependency
4. write the DDD vocabulary used in that slice
5. compare the same slice in another framework only after the first one is understandable

## What Belongs Elsewhere

- database catalog experiments belong in `learning-data-stores`
- frontend clients belong in `learning-frontend-typescript`
- CI, NGINX, deployment, and observability templates belong in `learning-platform-engineering`
- security testing labs belong in `learning-security-labs`

## Repository Profile

See [docs/repository-profile.md](docs/repository-profile.md) for GitHub description, topics, public safety notes, and first milestones.
