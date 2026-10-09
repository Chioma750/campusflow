import unittest

from campusflow.workflow import (
    assign_ticket,
    get_work_queue,
    update_status,
)
from tests.helpers import make_ticket


class TestTicketAssignment(unittest.TestCase):
    def setUp(self):
        self.ticket = make_ticket()
        self.tickets = {"T001": self.ticket}

    def test_assign_ticket_to_staff_member(self):
        result = assign_ticket(self.tickets, "T001", "Ada")

        self.assertEqual(result["assigned_to"], "Ada")
        self.assertEqual(self.ticket["assigned_to"], "Ada")

    def test_staff_name_is_trimmed(self):
        assign_ticket(self.tickets, "T001", "  Ada Lovelace  ")
        self.assertEqual(self.ticket["assigned_to"], "Ada Lovelace")

    def test_unknown_ticket_id_is_rejected(self):
        with self.assertRaises(KeyError):
            assign_ticket(self.tickets, "T999", "Ada")

    def test_blank_staff_name_is_rejected_without_mutation(self):
        for name in ("", "   ", "\t"):
            with self.subTest(name=name):
                before = self.ticket.copy()
                with self.assertRaises(ValueError):
                    assign_ticket(self.tickets, "T001", name)
                self.assertEqual(self.ticket, before)

    def test_resolved_ticket_cannot_be_assigned_or_reassigned(self):
        self.ticket["status"] = "resolved"
        self.ticket["assigned_to"] = "Ada"
        before = self.ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Grace")

        self.assertEqual(self.ticket, before)


class TestTicketWorkflow(unittest.TestCase):
    def setUp(self):
        self.ticket = make_ticket(assigned_to="Ada")
        self.tickets = {"T001": self.ticket}

    def test_assigned_open_ticket_can_move_to_in_progress(self):
        result = update_status(self.tickets, "T001", "in_progress")
        self.assertEqual(result["status"], "in_progress")

    def test_unassigned_ticket_cannot_move_to_in_progress(self):
        self.ticket["assigned_to"] = None
        before = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(self.ticket, before)

    def test_in_progress_ticket_can_be_resolved(self):
        self.ticket["status"] = "in_progress"
        result = update_status(self.tickets, "T001", "resolved")
        self.assertEqual(result["status"], "resolved")

    def test_resolved_ticket_can_only_be_reopened_to_open(self):
        self.ticket["status"] = "resolved"

        result = update_status(self.tickets, "T001", "open")

        self.assertEqual(result["status"], "open")

    def test_resolved_ticket_cannot_skip_reopen_step(self):
        self.ticket["status"] = "resolved"
        before = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

        self.assertEqual(self.ticket, before)

    def test_invalid_transition_is_rejected_without_mutation(self):
        before = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "resolved")

        self.assertEqual(self.ticket, before)

    def test_unknown_ticket_id_is_rejected(self):
        with self.assertRaises(KeyError):
            update_status(self.tickets, "T999", "in_progress")

    def test_invalid_status_value_is_rejected(self):
        before = self.ticket.copy()

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "closed")

        self.assertEqual(self.ticket, before)


class TestWorkQueue(unittest.TestCase):
    def setUp(self):
        self.tickets = {
            "T010": make_ticket(
                "T010", priority="low", status="open"
            ),
            "T003": make_ticket(
                "T003", priority="critical", status="open"
            ),
            "T002": make_ticket(
                "T002", priority="critical", status="in_progress"
            ),
            "T004": make_ticket(
                "T004", priority="high", status="open"
            ),
            "T001": make_ticket(
                "T001", priority="medium", status="resolved"
            ),
            "T006": make_ticket(
                "T006", priority="medium", status="open"
            ),
        }

    def test_queue_excludes_resolved_tickets(self):
        queue = get_work_queue(self.tickets)
        self.assertNotIn("T001", [ticket["id"] for ticket in queue])

    def test_queue_orders_priority_then_numeric_ticket_id(self):
        queue = get_work_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T003", "T004", "T006", "T010"],
        )

    def test_empty_queue_returns_empty_list(self):
        self.assertEqual(get_work_queue({}), [])


if __name__ == "__main__":
    unittest.main()
