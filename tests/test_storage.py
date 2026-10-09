import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import load_tickets, save_tickets
from tests.helpers import make_ticket


class TestTicketStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.file_path = Path(self.temp_dir.name) / "tickets.json"

    def test_save_and_load_preserves_ticket_data(self):
        tickets = {
            "T001": make_ticket("T001"),
            "T002": make_ticket(
                "T002",
                title="Printer issue",
                priority="medium",
                urgency="medium",
                affected_users=3,
                assigned_to="Ada",
                status="in_progress",
            ),
        }

        save_tickets(tickets, self.file_path)
        loaded = load_tickets(self.file_path)

        self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_collection(self):
        self.assertEqual(load_tickets(self.file_path), {})

    def test_malformed_json_raises_clear_error(self):
        self.file_path.write_text("{not valid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

    def test_saved_file_contains_json_object_keyed_by_ticket_id(self):
        tickets = {"T001": make_ticket("T001")}
        save_tickets(tickets, self.file_path)

        content = json.loads(self.file_path.read_text(encoding="utf-8"))

        self.assertIsInstance(content, dict)
        self.assertIn("T001", content)
        self.assertEqual(content["T001"]["id"], "T001")


if __name__ == "__main__":
    unittest.main()
