<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# DDD Tactical Core

A small **Orders** bounded context built with **DDD tactical patterns** in pure
Python (stdlib only, no framework). It exists so you can feel the vocabulary --
value object, entity, aggregate root, repository, application service, domain
event -- in code you can run and read in one sitting, *before* porting the same
model to Spring Boot.

This is the stdlib version of what `apps/spring-ddd` will become.

Last verified: 2026-06-21

## What's in here

| File | Tactical pattern |
| --- | --- |
| `orders.py` `Money` | Value object: immutable, currency-aware, equality by value, rejects negatives |
| `orders.py` `OrderLine` | Value object held inside the aggregate; subtotal is derived |
| `orders.py` `Order` | Aggregate root: identity, invariants, recomputed total, raises domain events |
| `orders.py` `OrderConfirmed` | Domain event (past tense, immutable) |
| `orders.py` `OrderRepository` / `InMemoryOrderRepository` | Repository: `Protocol` interface + in-memory impl |
| `orders.py` `PlaceOrder` | Application service / use case + event dispatch to subscribers |
| `test_orders.py` | `unittest` suite covering all of the above |

The enforced invariants on the `Order` aggregate:

- cannot confirm an **empty** order
- **total** is always recomputed from the lines, never a stored field
- **no mutation after confirmed** (add/remove/confirm all rejected)
- line currency must match the order currency
- adding an existing SKU merges quantities instead of duplicating

## Run

```bash
python3 projects/ddd-tactical-core/orders.py --demo
```

This runs the full `PlaceOrder` use case end to end: create a draft, add two
line items, confirm, and watch the `OrderConfirmed` domain event get dispatched
to a subscriber.

## Test

Non-interactive, exits non-zero on failure (so it works as a CI gate):

```bash
cd projects/ddd-tactical-core && python3 -m unittest -v
```

## Upgrade path

This project is deliberately framework-free. Each tactical piece maps directly
onto a **Spring Boot 4** (`apps/spring-ddd`) equivalent. When you build the
Spring version, swap each stdlib seam for the real tool below -- the domain
shape stays the same.

| This project (stdlib) | Spring Boot 4 equivalent |
| --- | --- |
| `Money` frozen dataclass | `@Embeddable` value type (e.g. a Java `record` mapped with `@Embeddable` / `@AttributeOverride`), embedded in the entity |
| `Order` aggregate root (plain class) | `@Entity` with `@Id`; `@OneToMany`/`@ElementCollection` for lines; invariants stay in the entity, not in the service |
| `OrderLine` value object | `@Embeddable` in an `@ElementCollection`, or a child `@Entity` owned by the aggregate |
| Recomputed `total()` | A `@Transient`/derived getter, or computed in the domain method -- never a persisted field that can drift |
| `OrderRepository` `Protocol` + `InMemoryOrderRepository` | `interface OrderRepository extends JpaRepository<Order, UUID>` (Spring Data generates the impl); swap the in-memory map for PostgreSQL |
| `OrderConfirmed` domain event | A plain event class; raised with `AbstractAggregateRoot.registerEvent(...)` or returned from the domain |
| `order.pull_events()` + `PlaceOrder._dispatch` | `ApplicationEventPublisher.publishEvent(...)`, or Spring Data's `@DomainEvents` / `@AfterDomainEventPublication` auto-publishing on `save` |
| Subscriber callables (`use_case.subscribe`) | `@EventListener` / `@TransactionalEventListener(phase = AFTER_COMMIT)` beans |
| `PlaceOrder` application service | `@Service @Transactional` class that loads via the repository, calls domain methods, and lets events publish on commit |
| `python3 -m unittest` | JUnit 5 + `@DataJpaTest` / `@SpringBootTest`, with Testcontainers PostgreSQL for integration tests |

Migration order that keeps tests green at every step:

1. Port `Money`, `OrderLine`, `Order`, and `OrderConfirmed` as plain Java
   classes/records with JUnit tests (no Spring yet) -- this is the
   `projects/java-ddd-slice` style.
2. Add JPA annotations and a Spring Data `OrderRepository`; keep an in-memory
   fake for unit tests, use Testcontainers for integration tests.
3. Replace manual event dispatch with `ApplicationEventPublisher` /
   `@TransactionalEventListener(AFTER_COMMIT)`.
4. Wrap the use case in `@Service @Transactional` and expose it over a
   controller in `apps/spring-ddd`.

## Exercises

Concrete next steps to deepen the model (each is a small, self-contained PR):

1. **Add an `OrderCancelled` domain event.** Implement `Order.cancel()` with the
   invariant that a *confirmed* order can be cancelled but a draft cannot, raise
   the event, and add a subscriber in `PlaceOrder` plus tests for both paths.
2. **Introduce a `Quantity` value object.** Replace the raw `int` quantity in
   `OrderLine` with a `Quantity` value object that rejects values `<= 0` and
   caps at a max (e.g. 999). Show how the invariant moves *down* into the value
   object, and that equality-by-value still holds.
3. **Enforce an aggregate-size invariant.** Reject orders with more than N
   distinct line items in `add_line`, and add a test proving the aggregate
   stays inside its consistency boundary.
4. **Add a real-ish persistence seam.** Write a second repository
   implementation, `JsonFileOrderRepository`, that serializes orders to a JSON
   file under `/tmp` (stdlib `json` only). Re-run the same `PlaceOrder` tests
   against both implementations to prove the domain does not depend on storage.
5. **Make event publishing transactional.** Change `PlaceOrder.confirm` so that
   if `repository.save` raises, *no* events are dispatched (publish-after-commit
   semantics). Add a failing-save test using a fake repository that throws.
