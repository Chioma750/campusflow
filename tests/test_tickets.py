import unittest

from campusflow.tickets import (
    create_ticket,
    get_ticket,
    list_tickets,
)
from tests.helpers import make_ticket


class TestTicketCreation(unittest.TestCase):
    def setUp(self):
        self.tickets = {}

    def test_create_ticket_stores_and_returns_ticket(self):
        ticket = create_ticket(
            self.tickets,
            "Campus Wi-Fi is down",
            "Network",
            "high",
            15,
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "Campus Wi-Fi is down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 15)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertIs(self.tickets["T001"], ticket)

    def test_ids_increment_from_existing_tickets(self):
        self.tickets["T001"] = make_ticket("T001")
        self.tickets["T004"] = make_ticket("T004")

        ticket = create_ticket(
            self.tickets, "Printer unavailable", "Hardware", "low", 1
        )

        self.assertEqual(ticket["id"], "T005")

    def test_blank_title_is_rejected(self):
        for title in ("", "   ", "\t"):
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    create_ticket(self.tickets, title, "Network", "low", 1)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Issue", "Facilities", "low", 1
            )

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Issue", "Network", "urgent", 1
            )

    def test_affected_users_must_be_positive_integer(self):
        for value in (0, -1, 1.5, "two", True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    create_ticket(
                        self.tickets, "Issue", "Network", "low", value
                    )

    def test_case_and_whitespace_are_normalized(self):
        ticket = create_ticket(
            self.tickets, "  Wi-Fi issue  ", " network ", " HIGH ", 2
        )

        self.assertEqual(ticket["title"], "Wi-Fi issue")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["priority"], "high")

    def test_priority_rules_and_boundaries(self):
        cases = [
            ("high", 10, "critical"),
            ("high", 1, "high"),
            ("low", 10, "high"),
            ("medium", 10, "high"),
            ("medium", 2, "medium"),
            ("low", 3, "medium"),
            ("low", 2, "low"),
        ]

        for urgency, affected_users, expected in cases:
            with self.subTest(
                urgency=urgency, affected_users=affected_users
            ):
                tickets = {}
                ticket = create_ticket(
                    tickets,
                    "Test issue",
                    "Network",
                    urgency,
                    affected_users,
                )
                self.assertEqual(ticket["priority"], expected)

    def test_invalid_creation_does_not_add_ticket(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "  ", "Network", "low", 1
            )
        self.assertEqual(self.tickets, {})


class TestTicketLookup(unittest.TestCase):
    def setUp(self):
        self.ticket = make_ticket()
        self.tickets = {"T001": self.ticket}

    def test_get_ticket_returns_matching_ticket(self):
        self.assertIs(get_ticket(self.tickets, "T001"), self.ticket)

    def test_get_ticket_raises_for_unknown_id(self):
        with self.assertRaises(KeyError):
            get_ticket(self.tickets, "T999")

    def test_list_tickets_returns_all_tickets(self):
        second = make_ticket("T002", title="Printer issue")
        self.tickets["T002"] = second

        result = list_tickets(self.tickets)

        self.assertEqual(len(result), 2)
        self.assertIn(self.ticket, result)
        self.assertIn(second, result)

    def test_list_tickets_returns_empty_list_for_empty_collection(self):
        self.assertEqual(list_tickets({}), [])


if __name__ == "__main__":
    unittest.main()
