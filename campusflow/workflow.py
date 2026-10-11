def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an existing, unresolved ticket to a staff member."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")

    ticket_id = ticket_id.strip().upper()

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff member name cannot be empty.")

    staff_name = staff_name.strip()

    ticket = tickets.get(ticket_id)

    if ticket is None:
        raise KeyError(f"Ticket '{ticket_id}' does not exist.")

    if ticket["status"].strip().lower() == "resolved":
        raise ValueError(
            "Cannot assign a resolved ticket. Reopen it first."
        )

    ticket["assigned_to"] = staff_name

    return ticket


def update_status(tickets, ticket_id, new_status):
    """Update a ticket status using the permitted workflow."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")

    ticket_id = ticket_id.strip().upper()

    if not isinstance(new_status, str) or not new_status.strip():
        raise ValueError("Status cannot be empty.")

    new_status = new_status.strip().lower()

    allowed_statuses = {"open", "in_progress", "resolved"}

    if new_status not in allowed_statuses:
        raise ValueError(f"Invalid status: '{new_status}'.")

    ticket = tickets.get(ticket_id)

    if ticket is None:
        raise KeyError(f"Ticket '{ticket_id}' does not exist.")

    current_status = ticket["status"].strip().lower()

    # Define permitted transitions.
    transitions = {
        "open": {"in_progress"},
        "in_progress": {"resolved"},
        "resolved": {"open"},
    }

    if new_status not in transitions[current_status]:
        raise ValueError(
            f"Cannot change status from '{current_status}' "
            f"to '{new_status}'."
        )

    # An unassigned ticket cannot enter active work.
    if new_status == "in_progress" and not (
        isinstance(ticket.get("assigned_to"), str)
        and ticket["assigned_to"].strip()
    ):
        raise ValueError(
            "A ticket must be assigned before work can begin."
        )

    ticket["status"] = new_status

    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets sorted by priority and ticket ID."""

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    queue = [
        ticket
        for ticket in tickets.values()
        if ticket["status"].strip().lower() != "resolved"
    ]

    def sort_key(ticket):
        ticket_id = ticket["id"].strip().upper()
        numeric_id = int(ticket_id[1:])

        priority = ticket["priority"].strip().lower()

        return (
            priority_order.get(priority, len(priority_order)),
            numeric_id,
        )

    return sorted(queue, key=sort_key)