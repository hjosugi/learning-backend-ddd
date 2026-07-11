<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Learning Backend DDD

Backend and DDD learning path across Spring Boot, Quarkus, Go/Gin, Phoenix, TypeScript service patterns, and local development services.

Last verified: 2026-06-21

## Development Environment

If Go, Java, Node.js, or Python are missing locally, enter the Nix shell:

```bash
nix develop
```

## Runnable Starter Project

Run the small JSON task API before moving to Spring, Quarkus, Go, or Phoenix:

```bash
python3 projects/task-api-stdlib/app.py --demo
python3 projects/task-api-stdlib/test_domain.py
```

To run the HTTP server:

```bash
python3 projects/task-api-stdlib/app.py
```

## Target Hands-On Projects

These projects use the actual backend learning targets, not just notes:

```bash
cd projects/go-http-api
go test ./...
```

```bash
cd projects/java-ddd-slice
javac *.java
java TaskPolicyTest
rm -f *.class
```

A stdlib DDD tactical core (Orders bounded context) that maps onto `apps/spring-ddd`:

```bash
python3 projects/ddd-tactical-core/orders.py --demo
cd projects/ddd-tactical-core && python3 -m unittest -v
```

GraphQL without API registration:

```bash
node projects/graphql-local-api/server.test.mjs
```

Local mail API boundary:

```bash
cd projects/local-mail-api-slice
javac *.java
java MailApiTest
rm -f *.class
```

Use these slices to learn handler boundaries, JSON contracts, Java domain modeling, DDD tactical patterns (entity, value object, aggregate, repository, application service, domain event), GraphQL resolver shape, local service doubles, and the code that should exist before adding Spring Boot, Quarkus, Apollo, GraphQL Yoga, or GreenMail adapters.

See [docs/learning-resources.md](docs/learning-resources.md) for curated DDD and Spring Boot references.

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

## License

0BSD. You can use, copy, modify, and distribute this project for almost any purpose.
