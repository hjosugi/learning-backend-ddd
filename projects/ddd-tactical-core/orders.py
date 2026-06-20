"""Orders bounded context, modeled with DDD tactical patterns (stdlib only).

This module is intentionally a single file so the whole bounded context reads
top-to-bottom. The sections map one-to-one onto DDD tactical building blocks:

    1. Money            -> value object (immutable, equality by value)
    2. OrderLine        -> value object held inside the aggregate
    3. OrderConfirmed   -> domain event
    4. Order            -> aggregate root (owns invariants + pending events)
    5. OrderRepository  -> repository (Protocol interface + in-memory impl)
    6. PlaceOrder       -> application service / use case + event dispatch

The point of this project is to feel the *vocabulary* of DDD in plain Python,
with no framework ceremony, before porting the same model to Spring Boot.
See README.md "Upgrade path" for the Spring Boot 4 mapping of each piece.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol
from uuid import UUID, uuid4

# ---------------------------------------------------------------------------
# 1. VALUE OBJECT: Money
# ---------------------------------------------------------------------------
# A value object has NO identity. Two Money instances are "the same" when their
# fields are equal, not because they are the same object. They are immutable:
# you never mutate Money, you compute a new Money. `frozen=True` gives us value
# equality, hashing, and immutability for free.


@dataclass(frozen=True)
class Money:
    """An immutable, currency-aware monetary amount.

    Amounts are stored as integer minor units (e.g. cents) to avoid float
    rounding error -- a classic value-object concern. 1050 + "USD" == $10.50.
    """

    amount: int  # minor units, e.g. cents; never floats
    currency: str = "USD"

    def __post_init__(self) -> None:
        # Invariants enforced at construction: a value object should never be
        # able to exist in an invalid state.
        if not isinstance(self.amount, int):
            raise TypeError("Money.amount must be an int (minor units, e.g. cents)")
        if self.amount < 0:
            raise ValueError("Money cannot be negative")
        if not self.currency or len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError("currency must be a 3-letter ISO code, e.g. 'USD'")
        # Normalize so USD and usd compare equal by value.
        object.__setattr__(self, "currency", self.currency.upper())

    @classmethod
    def zero(cls, currency: str = "USD") -> "Money":
        return cls(0, currency)

    def _assert_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"cannot combine {self.currency} with {other.currency}"
            )

    def add(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def times(self, quantity: int) -> "Money":
        if quantity < 0:
            raise ValueError("quantity cannot be negative")
        return Money(self.amount * quantity, self.currency)

    def __str__(self) -> str:
        return f"{self.amount / 100:.2f} {self.currency}"


# ---------------------------------------------------------------------------
# 2. VALUE OBJECT: OrderLine
# ---------------------------------------------------------------------------
# A line item is also a value object: it has no identity of its own and only
# matters as part of the Order aggregate. Its subtotal is derived, never stored.


@dataclass(frozen=True)
class OrderLine:
    sku: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        if not self.sku:
            raise ValueError("sku is required")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")

    def subtotal(self) -> Money:
        return self.unit_price.times(self.quantity)


# ---------------------------------------------------------------------------
# 3. DOMAIN EVENT: OrderConfirmed
# ---------------------------------------------------------------------------
# A domain event records that something meaningful happened *in the past*
# (note the past tense name). It is immutable and carries only the facts other
# parts of the system might react to. The aggregate raises it; the application
# service dispatches it.


@dataclass(frozen=True)
class OrderConfirmed:
    order_id: UUID
    total: Money
    line_count: int


# ---------------------------------------------------------------------------
# 4. AGGREGATE ROOT: Order
# ---------------------------------------------------------------------------
# The aggregate root is the ONLY entry point for changing anything inside the
# aggregate's consistency boundary. It:
#   - has identity (an id) and a mutable lifecycle, so it is an *entity*
#   - owns its OrderLine value objects
#   - protects invariants (no edits after confirmation, cannot confirm empty)
#   - records domain events into a pending list for the app service to publish
# Callers must NEVER reach inside and mutate _lines directly.


class Order:
    def __init__(self, customer_id: str, currency: str = "USD") -> None:
        if not customer_id:
            raise ValueError("customer_id is required")
        self.id: UUID = uuid4()
        self.customer_id = customer_id
        self.currency = currency.upper()
        self.confirmed = False
        self._lines: list[OrderLine] = []
        # Pending domain events live here until the application service drains
        # them. The aggregate never dispatches events itself -- that keeps the
        # domain free of infrastructure concerns.
        self._pending_events: list[object] = []

    # --- queries ----------------------------------------------------------

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        # Expose a read-only view so callers cannot mutate internal state.
        return tuple(self._lines)

    def total(self) -> Money:
        # Total is ALWAYS recomputed from the lines; it is never a stored field
        # that could drift out of sync (an invariant by construction).
        running = Money.zero(self.currency)
        for line in self._lines:
            running = running.add(line.subtotal())
        return running

    def is_empty(self) -> bool:
        return len(self._lines) == 0

    # --- commands ---------------------------------------------------------

    def add_line(self, sku: str, unit_price: Money, quantity: int) -> None:
        self._guard_mutable()
        if unit_price.currency != self.currency:
            raise ValueError(
                f"line currency {unit_price.currency} does not match "
                f"order currency {self.currency}"
            )
        # If the SKU already exists, merge quantities rather than duplicating --
        # this is an aggregate-level invariant about how lines compose.
        for index, existing in enumerate(self._lines):
            if existing.sku == sku:
                self._lines[index] = OrderLine(
                    sku, unit_price, existing.quantity + quantity
                )
                return
        self._lines.append(OrderLine(sku, unit_price, quantity))

    def remove_line(self, sku: str) -> None:
        self._guard_mutable()
        self._lines = [line for line in self._lines if line.sku != sku]

    def confirm(self) -> None:
        """Transition to confirmed, enforcing invariants and raising an event."""
        self._guard_mutable()
        if self.is_empty():
            raise ValueError("cannot confirm an empty order")
        self.confirmed = True
        # Record (do not dispatch) the domain event.
        self._pending_events.append(
            OrderConfirmed(
                order_id=self.id,
                total=self.total(),
                line_count=len(self._lines),
            )
        )

    # --- domain-event plumbing -------------------------------------------

    def pull_events(self) -> list[object]:
        """Return and clear pending events; called by the application service."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- invariants -------------------------------------------------------

    def _guard_mutable(self) -> None:
        # No mutation after the order is confirmed: a confirmed order is a
        # committed fact, so the aggregate refuses further changes.
        if self.confirmed:
            raise ValueError("order is confirmed and can no longer be modified")

    def __repr__(self) -> str:
        return (
            f"Order(id={self.id}, customer={self.customer_id}, "
            f"lines={len(self._lines)}, total={self.total()}, "
            f"confirmed={self.confirmed})"
        )


# ---------------------------------------------------------------------------
# 5. REPOSITORY: interface + in-memory implementation
# ---------------------------------------------------------------------------
# A repository gives the illusion of an in-memory collection of aggregates.
# The domain depends only on the interface (Protocol); infrastructure provides
# the concrete store. This is the seam you later replace with a real database.


class OrderRepository(Protocol):
    def get(self, order_id: UUID) -> Order: ...

    def save(self, order: Order) -> None: ...

    def all(self) -> list[Order]: ...


class InMemoryOrderRepository:
    """A dict-backed repository -- perfect for tests and for learning."""

    def __init__(self) -> None:
        self._store: dict[UUID, Order] = {}

    def get(self, order_id: UUID) -> Order:
        if order_id not in self._store:
            raise KeyError(f"order {order_id} not found")
        return self._store[order_id]

    def save(self, order: Order) -> None:
        self._store[order.id] = order

    def all(self) -> list[Order]:
        return list(self._store.values())


# ---------------------------------------------------------------------------
# 6. APPLICATION SERVICE: PlaceOrder use case + event dispatch
# ---------------------------------------------------------------------------
# The application service orchestrates a single use case. It is thin: it loads
# the aggregate, invokes domain behavior, persists via the repository, and then
# dispatches whatever domain events the aggregate recorded. It holds NO domain
# rules itself -- those belong on the aggregate.

# A subscriber is any callable that reacts to a published domain event.
Subscriber = Callable[[object], None]


@dataclass
class PlaceOrder:
    repository: OrderRepository
    subscribers: list[Subscriber] = field(default_factory=list)

    def subscribe(self, handler: Subscriber) -> None:
        self.subscribers.append(handler)

    def create_draft(self, customer_id: str, currency: str = "USD") -> UUID:
        order = Order(customer_id, currency)
        self.repository.save(order)
        return order.id

    def add_item(
        self, order_id: UUID, sku: str, unit_price: Money, quantity: int
    ) -> None:
        order = self.repository.get(order_id)
        order.add_line(sku, unit_price, quantity)
        self.repository.save(order)

    def confirm(self, order_id: UUID) -> Money:
        """Confirm an order, then publish its domain events to subscribers."""
        order = self.repository.get(order_id)
        order.confirm()
        self.repository.save(order)
        # Drain and dispatch AFTER the state change is persisted, mirroring the
        # "publish after commit" pattern you would use with a real transaction.
        self._dispatch(order.pull_events())
        return order.total()

    def _dispatch(self, events: list[object]) -> None:
        for event in events:
            for handler in self.subscribers:
                handler(event)


# ---------------------------------------------------------------------------
# DEMO: run the whole use case end to end (`python3 orders.py --demo`)
# ---------------------------------------------------------------------------


def demo() -> None:
    repo = InMemoryOrderRepository()
    use_case = PlaceOrder(repository=repo)

    # A subscriber that reacts to the OrderConfirmed domain event. In Spring
    # this is an @EventListener; here it is just a function.
    confirmations: list[OrderConfirmed] = []
    use_case.subscribe(
        lambda event: confirmations.append(event)
        if isinstance(event, OrderConfirmed)
        else None
    )

    order_id = use_case.create_draft("customer-42", currency="USD")
    use_case.add_item(order_id, sku="BOOK-DDD", unit_price=Money(4599), quantity=2)
    use_case.add_item(order_id, sku="MUG", unit_price=Money(1200), quantity=1)
    total = use_case.confirm(order_id)

    print(f"order total: {total}")
    print(f"events published: {confirmations}")
    print(f"persisted order: {repo.get(order_id)}")


if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        demo()
    else:
        print("run `python3 orders.py --demo` or `python3 test_orders.py`")
