"""unittest suite for the Orders bounded context.

Coverage is grouped by tactical pattern so each test documents one DDD idea:
value-object equality, aggregate invariants, domain-event emission, and the
PlaceOrder application service. Run non-interactively with:

    python3 -m unittest -v

(exits non-zero on failure, so it works as a CI gate).
"""

from __future__ import annotations

import unittest
from uuid import UUID

from orders import (
    InMemoryOrderRepository,
    Money,
    Order,
    OrderConfirmed,
    OrderLine,
    PlaceOrder,
)


class MoneyValueObjectTests(unittest.TestCase):
    """Value object: equality by value, immutability, currency awareness."""

    def test_equality_by_value(self) -> None:
        # Two separately-constructed Money objects with the same fields are
        # equal -- that is the defining trait of a value object.
        self.assertEqual(Money(1050, "USD"), Money(1050, "USD"))
        self.assertEqual(hash(Money(1050, "USD")), hash(Money(1050, "USD")))

    def test_currency_normalized_for_equality(self) -> None:
        self.assertEqual(Money(500, "usd"), Money(500, "USD"))

    def test_inequality_on_amount_or_currency(self) -> None:
        self.assertNotEqual(Money(1050, "USD"), Money(1051, "USD"))
        self.assertNotEqual(Money(1050, "USD"), Money(1050, "EUR"))

    def test_rejects_negative_amount(self) -> None:
        with self.assertRaises(ValueError):
            Money(-1, "USD")

    def test_rejects_bad_currency(self) -> None:
        with self.assertRaises(ValueError):
            Money(100, "DOLLARS")

    def test_is_immutable(self) -> None:
        price = Money(100, "USD")
        with self.assertRaises(Exception):
            price.amount = 200  # type: ignore[misc]

    def test_arithmetic_returns_new_value(self) -> None:
        a = Money(100, "USD")
        b = a.add(Money(50, "USD"))
        self.assertEqual(b, Money(150, "USD"))
        self.assertEqual(a, Money(100, "USD"))  # original untouched
        self.assertEqual(Money(100, "USD").times(3), Money(300, "USD"))

    def test_cannot_add_across_currencies(self) -> None:
        with self.assertRaises(ValueError):
            Money(100, "USD").add(Money(100, "EUR"))


class OrderLineTests(unittest.TestCase):
    def test_subtotal_is_derived(self) -> None:
        line = OrderLine("SKU-1", Money(250, "USD"), 4)
        self.assertEqual(line.subtotal(), Money(1000, "USD"))

    def test_rejects_non_positive_quantity(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine("SKU-1", Money(250, "USD"), 0)


class OrderAggregateTests(unittest.TestCase):
    """Aggregate root: identity, invariants, recomputed total, lifecycle."""

    def test_has_identity(self) -> None:
        order = Order("customer-1")
        self.assertIsInstance(order.id, UUID)
        # Two orders for the same customer are different entities.
        self.assertNotEqual(order.id, Order("customer-1").id)

    def test_total_is_recomputed_from_lines(self) -> None:
        order = Order("customer-1")
        order.add_line("BOOK", Money(4599, "USD"), 2)
        order.add_line("MUG", Money(1200, "USD"), 1)
        self.assertEqual(order.total(), Money(10398, "USD"))

    def test_adding_same_sku_merges_quantity(self) -> None:
        order = Order("customer-1")
        order.add_line("MUG", Money(1200, "USD"), 1)
        order.add_line("MUG", Money(1200, "USD"), 2)
        self.assertEqual(len(order.lines), 1)
        self.assertEqual(order.total(), Money(3600, "USD"))

    def test_line_currency_must_match_order(self) -> None:
        order = Order("customer-1", currency="USD")
        with self.assertRaises(ValueError):
            order.add_line("MUG", Money(1200, "EUR"), 1)

    def test_lines_view_is_read_only(self) -> None:
        order = Order("customer-1")
        order.add_line("MUG", Money(1200, "USD"), 1)
        # `lines` is a tuple snapshot -- callers cannot mutate internals.
        self.assertIsInstance(order.lines, tuple)

    def test_cannot_confirm_empty_order(self) -> None:
        order = Order("customer-1")
        with self.assertRaises(ValueError):
            order.confirm()
        self.assertFalse(order.confirmed)

    def test_no_mutation_after_confirmed(self) -> None:
        order = Order("customer-1")
        order.add_line("MUG", Money(1200, "USD"), 1)
        order.confirm()
        self.assertTrue(order.confirmed)
        with self.assertRaises(ValueError):
            order.add_line("BOOK", Money(4599, "USD"), 1)
        with self.assertRaises(ValueError):
            order.remove_line("MUG")
        with self.assertRaises(ValueError):
            order.confirm()


class DomainEventTests(unittest.TestCase):
    """Domain event: emitted into the pending list, drained once."""

    def test_confirm_records_order_confirmed_event(self) -> None:
        order = Order("customer-1")
        order.add_line("MUG", Money(1200, "USD"), 2)
        order.confirm()
        events = order.pull_events()
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertIsInstance(event, OrderConfirmed)
        self.assertEqual(event.order_id, order.id)
        self.assertEqual(event.total, Money(2400, "USD"))
        self.assertEqual(event.line_count, 1)

    def test_events_are_drained_only_once(self) -> None:
        order = Order("customer-1")
        order.add_line("MUG", Money(1200, "USD"), 1)
        order.confirm()
        self.assertEqual(len(order.pull_events()), 1)
        self.assertEqual(len(order.pull_events()), 0)  # second pull is empty

    def test_no_event_when_confirmation_fails(self) -> None:
        order = Order("customer-1")  # empty -> confirm raises
        with self.assertRaises(ValueError):
            order.confirm()
        self.assertEqual(order.pull_events(), [])


class InMemoryRepositoryTests(unittest.TestCase):
    def test_save_and_get_roundtrip(self) -> None:
        repo = InMemoryOrderRepository()
        order = Order("customer-1")
        repo.save(order)
        self.assertIs(repo.get(order.id), order)
        self.assertEqual(len(repo.all()), 1)

    def test_get_missing_raises(self) -> None:
        repo = InMemoryOrderRepository()
        with self.assertRaises(KeyError):
            repo.get(Order("x").id)


class PlaceOrderUseCaseTests(unittest.TestCase):
    """Application service: orchestration + event dispatch to subscribers."""

    def setUp(self) -> None:
        self.repo = InMemoryOrderRepository()
        self.use_case = PlaceOrder(repository=self.repo)
        self.received: list[object] = []
        self.use_case.subscribe(self.received.append)

    def test_full_place_order_flow(self) -> None:
        order_id = self.use_case.create_draft("customer-99", currency="USD")
        self.use_case.add_item(order_id, "BOOK", Money(4599, "USD"), 2)
        self.use_case.add_item(order_id, "MUG", Money(1200, "USD"), 1)
        total = self.use_case.confirm(order_id)

        self.assertEqual(total, Money(10398, "USD"))
        # The persisted aggregate reflects the confirmation.
        self.assertTrue(self.repo.get(order_id).confirmed)

    def test_confirm_dispatches_event_to_subscriber(self) -> None:
        order_id = self.use_case.create_draft("customer-99")
        self.use_case.add_item(order_id, "MUG", Money(1200, "USD"), 3)
        self.use_case.confirm(order_id)

        self.assertEqual(len(self.received), 1)
        self.assertIsInstance(self.received[0], OrderConfirmed)
        self.assertEqual(self.received[0].total, Money(3600, "USD"))

    def test_multiple_subscribers_all_notified(self) -> None:
        second: list[object] = []
        self.use_case.subscribe(second.append)
        order_id = self.use_case.create_draft("customer-99")
        self.use_case.add_item(order_id, "MUG", Money(1200, "USD"), 1)
        self.use_case.confirm(order_id)

        self.assertEqual(len(self.received), 1)
        self.assertEqual(len(second), 1)

    def test_confirming_empty_order_raises_and_publishes_nothing(self) -> None:
        order_id = self.use_case.create_draft("customer-99")
        with self.assertRaises(ValueError):
            self.use_case.confirm(order_id)
        self.assertEqual(self.received, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
