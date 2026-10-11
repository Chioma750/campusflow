
import unittest
from unittest.mock import patch

import main


class TestMainMenu(unittest.TestCase):

    @patch("main.save_application_data")
    @patch("main.load_application_data", return_value={})
    def test_invalid_option_returns_to_menu(
        self, mock_load, mock_save
    ):
        with patch("builtins.input", side_effect=["9", "0"]):
            with patch("builtins.print") as mock_print:
                main.main()

        printed_messages = [
            str(call) for call in mock_print.call_args_list
        ]

        self.assertTrue(
            any("Invalid option" in message for message in printed_messages)
        )
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({})

    @patch("main.save_application_data")
    @patch("main.load_application_data", return_value={})
    def test_exit_saves_tickets(
        self, mock_load, mock_save
    ):
        with patch("builtins.input", return_value="0"):
            with patch("builtins.print"):
                main.main()

        mock_load.assert_called_once()
        mock_save.assert_called_once_with({})

    @patch("main.save_application_data")
    @patch("main.load_application_data", return_value={})
    def test_create_ticket_through_menu(
        self, mock_load, mock_save
    ):
        user_inputs = [
            "1",                    # Create ticket
            "Campus Wi-Fi is down",
            "Network",
            "high",
            "15",
            "0",                    # Save and exit
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print"):
                main.main()

        mock_load.assert_called_once()

        saved_tickets = mock_save.call_args.args[0]

        self.assertEqual(len(saved_tickets), 1)
        ticket = saved_tickets["T001"]
        self.assertEqual(ticket["title"], "Campus Wi-Fi is down")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

        # One save after creation and another on exit.
        self.assertEqual(mock_save.call_count, 2)


    @patch("main.save_application_data")
    @patch("main.load_application_data")
    def test_assign_and_update_ticket_through_menu(
        self, mock_load, mock_save
    ):
        tickets = {
            "T001": {
                "id": "T001",
                "title": "Network down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        }
        mock_load.return_value = tickets

        user_inputs = [
            "4",       # Assign ticket
            "T001",
            "Ada",
            "5",       # Update status
            "T001",
            "in_progress",
            "0",       # Save and exit
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print"):
                main.main()

        self.assertEqual(tickets["T001"]["assigned_to"], "Ada")
        self.assertEqual(tickets["T001"]["status"], "in_progress")

        # Assignment, status update, and exit each trigger a save.
        self.assertEqual(mock_save.call_count, 3)

    @patch("main.save_application_data")
    @patch("main.load_application_data")
    def test_work_queue_and_reports_through_menu(
        self, mock_load, mock_save
    ):
        tickets = {
            "T001": {
                "id": "T001",
                "title": "Network down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": "Ada",
            },
            "T002": {
                "id": "T002",
                "title": "Resolved laptop issue",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "resolved",
                "assigned_to": "John",
            },
        }
        mock_load.return_value = tickets

        user_inputs = [
            "6",  # View work queue
            "7",  # View reports
            "0",  # Save and exit
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print") as mock_print:
                main.main()

        printed_output = "\n".join(
            " ".join(str(arg) for arg in call.args)
            for call in mock_print.call_args_list
        )

        # The open ticket appears in the work queue.
        self.assertIn("Network down", printed_output)

        # The resolved ticket should not appear in the work queue.
        self.assertNotIn("Resolved laptop issue", printed_output)

        # Reports should include both tickets in the total.
        self.assertIn("CampusFlow Reports", printed_output)
        self.assertIn("'total': 2", printed_output)

        # Exiting the application saves the ticket collection.
        mock_save.assert_called_once_with(tickets)

    @patch("main.save_application_data")
    @patch("main.load_application_data")
    def test_work_queue_order_and_reports(
        self, mock_load, mock_save
    ):
        tickets = {
            "T001": {
                "id": "T001",
                "title": "Low priority issue",
                "category": "Other",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "open",
                "assigned_to": "Ada",
            },
            "T002": {
                "id": "T002",
                "title": "Critical network issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": "John",
            },
            "T003": {
                "id": "T003",
                "title": "Resolved laptop issue",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
                "priority": "low",
                "status": "resolved",
                "assigned_to": "Grace",
            },
        }
        mock_load.return_value = tickets

        user_inputs = ["6", "7", "0"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print") as mock_print:
                main.main()

        output = "\n".join(
            " ".join(str(arg) for arg in call.args)
            for call in mock_print.call_args_list
        )

        critical_position = output.index("Critical network issue")
        low_position = output.index("Low priority issue")

        self.assertLess(critical_position, low_position)
        self.assertNotIn("Resolved laptop issue", output)
        self.assertIn("CampusFlow Reports", output)
        self.assertIn("'total': 3", output)
        mock_save.assert_called_once_with(tickets)

    @patch("main.save_application_data")
    @patch("main.load_application_data", return_value={})
    def test_empty_reports_through_menu(
        self, mock_load, mock_save
    ):
        with patch("builtins.input", side_effect=["7", "0"]):
            with patch("builtins.print") as mock_print:
                main.main()

        output = "\n".join(
            " ".join(str(arg) for arg in call.args)
            for call in mock_print.call_args_list
        )

        self.assertIn("CampusFlow Reports", output)
        self.assertIn("'total': 0", output)
        mock_save.assert_called_once_with({})

    @patch("main.save_application_data")
    @patch("main.load_application_data")
    def test_view_existing_and_unknown_ticket(
        self, mock_load, mock_save
    ):
        tickets = {
            "T001": {
                "id": "T001",
                "title": "Campus Wi-Fi issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        }
        mock_load.return_value = tickets

        user_inputs = [
            "3", "T001",
            "3", "T999",
            "0",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print") as mock_print:
                main.main()

        output = "\n".join(
            " ".join(str(arg) for arg in call.args)
            for call in mock_print.call_args_list
        )

        self.assertIn("Campus Wi-Fi issue", output)
        self.assertIn("does not exist", output)
        mock_save.assert_called_once_with(tickets)

    @patch("main.save_application_data")
    @patch("main.load_application_data", return_value={})
    def test_invalid_ticket_input_does_not_crash_menu(
        self, mock_load, mock_save
    ):
        user_inputs = [
            "1",
            "   ",       # Blank title should fail validation.
            "Network",
            "high",
            "15",
            "0",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print") as mock_print:
                main.main()

        output = "\n".join(
            " ".join(str(arg) for arg in call.args)
            for call in mock_print.call_args_list
        )

        self.assertIn("Operation failed:", output)
        self.assertIn("Ticket title cannot be blank.", output)
        mock_load.assert_called_once()
        mock_save.assert_called_once_with({})

    @patch("main.save_application_data")
    @patch("main.load_application_data")
    def test_reopen_resolved_ticket_before_reassignment(
        self, mock_load, mock_save
    ):
        tickets = {
            "T001": {
                "id": "T001",
                "title": "Resolved network issue",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "resolved",
                "assigned_to": "Ada",
            }
        }
        mock_load.return_value = tickets

        user_inputs = [
            "5", "T001", "open",  # Explicitly reopen.
            "4", "T001", "Grace",  # Reassign after reopening.
            "0",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print"):
                main.main()

        self.assertEqual(tickets["T001"]["status"], "open")
        self.assertEqual(tickets["T001"]["assigned_to"], "Grace")
        self.assertEqual(mock_save.call_count, 3)

    @patch("main.load_tickets", side_effect=FileNotFoundError)
    def test_missing_saved_file_starts_with_empty_tickets(
        self, mock_load_tickets
    ):
        tickets = main.load_application_data()

        self.assertEqual(tickets, {})
        mock_load_tickets.assert_called_once_with(main.DATA_FILE)


if __name__ == "__main__":
    unittest.main()
