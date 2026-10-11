
from pathlib import Path
from campusflow.tickets import (
    create_ticket,
    get_ticket,
    list_tickets,
)
from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_work_queue,
)
from campusflow.storage import load_tickets, save_tickets
from campusflow.reports import generate_report


DATA_FILE = Path(__file__).resolve().parent / "data" / "tickets.json"


def load_application_data():
    """Load saved tickets, starting with an empty collection if none exist."""
    try:
        return load_tickets(DATA_FILE)
    except FileNotFoundError:
        return {}


def save_application_data(tickets):
    """Persist tickets to the configured JSON file."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    save_tickets(tickets, DATA_FILE)


def display_ticket(ticket):
    """Display a ticket's fields in a readable format."""
    if not ticket:
        print("Ticket not found.")
        return

    for field, value in ticket.items():
        print(f"{field.replace('_', ' ').title()}: {value}")


def handle_create(tickets):
    title = input("Ticket title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    affected_users = input("Number of affected users: ")

    ticket = create_ticket(
        tickets,
        title,
        category,
        urgency,
        affected_users,
    )
    save_application_data(tickets)
    print(f"\nTicket {ticket['id']} created successfully.")


def handle_list(tickets):
    all_tickets = list_tickets(tickets)

    if not all_tickets:
        print("No tickets found.")
        return

    for ticket in all_tickets:
        display_ticket(ticket)
        print("-" * 35)


def handle_view(tickets):
    ticket_id = input("Enter ticket ID: ").strip().upper()
    display_ticket(get_ticket(tickets, ticket_id))


def handle_assign(tickets):
    ticket_id = input("Enter ticket ID: ").strip().upper()
    staff_name = input("Staff member's name: ")

    assign_ticket(tickets, ticket_id, staff_name)
    save_application_data(tickets)
    print("Ticket assignment completed.")


def handle_status(tickets):
    ticket_id = input("Enter ticket ID: ").strip().upper()
    print("Available statuses: open, in_progress, resolved")
    new_status = input("Enter the new status: ").strip().lower()

    update_status(tickets, ticket_id, new_status)
    save_application_data(tickets)
    print("Ticket status updated.")


def handle_queue(tickets):
    queue = get_work_queue(tickets)

    if not queue:
        print("No tickets in the work queue.")
        return

    for ticket in queue:
        display_ticket(ticket)
        print("-" * 35)


def handle_reports(tickets):
    report = generate_report(tickets)
    print("\nCampusFlow Reports")
    print("=" * 35)
    print(report)


def main():
    tickets = load_application_data()

    actions = {
        "1": ("Create ticket", handle_create),
        "2": ("List all tickets", handle_list),
        "3": ("View ticket details", handle_view),
        "4": ("Assign ticket", handle_assign),
        "5": ("Update ticket status / reopen", handle_status),
        "6": ("View work queue", handle_queue),
        "7": ("View reports", handle_reports),
    }

    while True:
        print("\n=== CampusFlow Ticket Manager ===")

        for option, (label, _) in actions.items():
            print(f"{option}. {label}")

        print("0. Save and exit")

        choice = input("Select an option: ").strip()

        if choice == "0":
            save_application_data(tickets)
            print("Tickets saved. Goodbye!")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid option. Please choose a listed option.")
            continue

        try:
            action[1](tickets)
        except (ValueError, KeyError, FileNotFoundError) as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()
