import unittest

from campusflow.reports import generate_report
from tests.helpers import make_ticket


class TestTicketReports(unittest.TestCase):
    def test_empty_collection_returns_zero_totals(self):
        report = generate_report({})

        self.assertEqual(report["total"], 0)
        self.assertEqual(
            report["by_status"],
            {"open": 0, "in_progress": 0, "resolved": 0},
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 0, "high": 0, "medium": 0, "low": 0},
        )

    def test_report_counts_statuses_and_priorities(self):
        tickets = {
            "T001": make_ticket(
                "T001", priority="critical", status="open"
            ),
            "T002": make_ticket(
                "T002", priority="high", status="in_progress"
            ),
            "T003": make_ticket(
                "T003", priority="medium", status="resolved"
            ),
            "T004": make_ticket(
                "T004", priority="low", status="open"
            ),
        }

        report = generate_report(tickets)

        self.assertEqual(report["total"], 4)
        self.assertEqual(
            report["by_status"],
            {"open": 2, "in_progress": 1, "resolved": 1},
        )
        self.assertEqual(
            report["by_priority"],
            {"critical": 1, "high": 1, "medium": 1, "low": 1},
        )

    def test_report_includes_zero_count_categories(self):
        tickets = {
            "T001": make_ticket("T001", priority="critical", status="open")
        }

        report = generate_report(tickets)

        self.assertEqual(report["by_status"]["resolved"], 0)
        self.assertEqual(report["by_priority"]["low"], 0)


if __name__ == "__main__":
    unittest.main()
