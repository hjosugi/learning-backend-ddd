<!-- i18n: language-switcher -->
[English](learning-resources.md) | [日本語](learning-resources.ja.md)

# Further learning resources

Last verified: 2026-06-21

Curated, canonical primary sources for this repo's named learning technology:
**DDD tactical patterns** (entity, value object, aggregate, repository,
application service, domain event) and the **Spring Boot / Java** stack they get
ported onto. Links prefer the documentation root over deep guessed paths.

## DDD tactical patterns

- **Domain-Driven Design: Tackling Complexity in the Heart of Software** -- Eric Evans (the "blue book").
  <https://www.domainlanguage.com/ddd/>
  The original source for entity, value object, aggregate, repository, and
  domain event. The vocabulary this whole repo is built around.

- **Implementing Domain-Driven Design** -- Vaughn Vernon (the "red book").
  <https://www.informit.com/store/implementing-domain-driven-design-9780321834577>
  The most practical, code-first treatment of aggregates, repositories, and
  domain events; closest to how you'd actually structure `ddd-tactical-core`.

- **Domain-Driven Design Reference** -- Eric Evans (free condensed definitions).
  <https://www.domainlanguage.com/ddd/reference/>
  A short, authoritative glossary of the tactical building blocks -- ideal when
  you want the precise definition of "aggregate root" or "value object".

- **DDD Aggregate** -- Martin Fowler.
  <https://martinfowler.com/bliki/DDD_Aggregate.html>
  A crisp, widely-cited explanation of aggregate boundaries and why the root is
  the only entry point -- exactly the invariant the `Order` class enforces.

## Spring Boot / Java (the upgrade target)

- **Spring Boot Reference Documentation**.
  <https://docs.spring.io/spring-boot/>
  Official docs for the framework `apps/spring-ddd` will use; start here for
  `@Service`, configuration, and testing slices.

- **Spring Data JPA Reference**.
  <https://spring.io/projects/spring-data-jpa>
  The repository abstraction (`JpaRepository`) plus `@DomainEvents` /
  `@AfterDomainEventPublication` for auto-publishing aggregate events on save.

- **Spring Framework Reference -- Application Events**.
  <https://docs.spring.io/spring-framework/reference/>
  `ApplicationEventPublisher`, `@EventListener`, and
  `@TransactionalEventListener` -- the production replacement for this project's
  manual `subscribe` / `_dispatch` event mechanism.

- **Spring Modulith**.
  <https://spring.io/projects/spring-modulith>
  Module boundaries and event-driven communication between bounded contexts;
  the natural next step after a single tactical core.

- **Jakarta Persistence (JPA) Specification**.
  <https://jakarta.ee/specifications/persistence/>
  The standard behind `@Entity`, `@Embeddable`, and `@ElementCollection` used to
  map aggregates and value objects in the Spring port.

## Python (this implementation)

- **Python `dataclasses` documentation**.
  <https://docs.python.org/3/library/dataclasses.html>
  `frozen=True` for immutable value objects with value equality and hashing --
  the basis of `Money` and `OrderLine`.

- **Python `unittest` documentation**.
  <https://docs.python.org/3/library/unittest.html>
  The stdlib test framework used by `test_orders.py`; the conceptual analogue of
  JUnit 5 in the Spring port.

- **Python `typing.Protocol`**.
  <https://docs.python.org/3/library/typing.html>
  Structural interfaces used to define `OrderRepository` without inheritance --
  the seam Spring Data later implements for you.
