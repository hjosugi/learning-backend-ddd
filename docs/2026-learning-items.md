# 2026 Learning Items: Backend and DDD

Last verified: 2026-06-20

## Must Learn

### API design

- request/response models
- validation errors
- pagination and filtering
- idempotency
- authentication boundaries
- OpenAPI documentation

Projects:

- Move `tasklist` into `apps/spring-tasklist`.
- Move `gin-sample` into `apps/gin-api`.

### Spring Boot 4 and Java

- Spring Boot 4.1
- Java 21/25
- Spring MVC/JPA
- WebFlux/R2DBC
- Spring Modulith basics
- Actuator health and metrics

Projects:

- Move `ddd-spring-boot` into `apps/spring-ddd`.
- Move `flux-sample` into `apps/spring-webflux-r2dbc`.

### Local development services

- embedded service for local integration tests
- profile separation
- test-only dependencies
- no external credentials for local dev

Projects:

- Move `local-mail-api` into `apps/local-mail-api` or `lessons/local-mail-api`.
- Use it as a Spring Boot + GreenMail lesson.

### DDD and architecture

- entity
- value object
- aggregate
- repository
- application service
- domain event
- module boundary
- anti-corruption layer

Projects:

- Add `docs/ddd-vocabulary.md`.
- Add the same use case in Spring, Quarkus, and Go.

### Framework comparison

- Spring Boot
- Quarkus
- Go/Gin
- Phoenix
- TypeScript service model

Projects:

- Move `quarkus-ddd` into `apps/quarkus-ddd`.
- Keep `realworld-phx` as `reading/phoenix-realworld`.

## Definition of Done

- Every app has a run command.
- Every app has at least one integration test or documented manual curl flow.
- Every app documents local dependencies.
- Every framework comparison includes tradeoffs.

