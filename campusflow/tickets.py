def validate_title(raw_title):
    cleaned_title = raw_title.strip()
    if cleaned_title == "":
        raise ValueError("Ticket title cannot be blank.")
    return cleaned_title

def validate_category(raw_category):
    cleaned_category = raw_category.strip().title()
    category = ["Network", "Hardware", "Software", "Other"]
    if cleaned_category not in category:
        raise ValueError("Invalid category. Must be Network, Hardware, Software, or Other.")
    return cleaned_category

def validate_urgency(raw_urgency):
    cleaned_urgency = raw_urgency.strip().lower()
    validate = ["low", "medium", "high"]
    if cleaned_urgency not in validate:
        raise ValueError("Invalid urgency. Must be low, medium, or high.")
    return cleaned_urgency


def validate_users(raw_users):
    if isinstance(raw_users, bool):
        raise ValueError("Affected users must be a positive integer.")

    try:
        num_users = int(raw_users)
    except (ValueError, TypeError):
        raise ValueError(
            "Affected users must be a valid whole number."
        ) from None

    if isinstance(raw_users, float) and not raw_users.is_integer():
        raise ValueError("Affected users must be a positive integer.")

    if isinstance(raw_users, str) and str(num_users) != raw_users.strip():
        raise ValueError("Affected users must be a valid whole number.")

    if num_users <= 0:
        raise ValueError(
            "Affected users must be a positive integer greater than zero."
        )

    return num_users



def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"



def generate_id(current_tickets):
    if not current_tickets:
        return "T001"

    ticket_numbers = [
        int(ticket_id[1:])
        for ticket_id in current_tickets
        if ticket_id.startswith("T") and ticket_id[1:].isdigit()
    ]

    next_number = max(ticket_numbers, default=0) + 1
    return f"T{next_number:03d}"


def create_ticket(current_tickets, raw_title, raw_category, raw_urgency, raw_users):
    valid_title = validate_title(raw_title)
    valid_category = validate_category(raw_category)
    valid_urgency = validate_urgency(raw_urgency)
    valid_users = validate_users(raw_users)

    computed_priority = calculate_priority(valid_urgency, valid_users)
    new_id = generate_id(current_tickets)

    new_tickets = {
        "id": new_id,
        "title": valid_title,
        "category": valid_category,
        "urgency": valid_urgency,
        "affected_users": valid_users,
        "priority": computed_priority,
        "status": "open",
        "assigned_to": None
    }

    current_tickets[new_id] = new_tickets

    return new_tickets


def get_ticket(tickets, ticket_id):
    """Return a ticket by its ID or raise KeyError if it does not exist."""
    ticket_id = ticket_id.strip().upper()

    if ticket_id not in tickets:
        raise KeyError(f"Ticket '{ticket_id}' does not exist.")

    return tickets[ticket_id]


def list_tickets(tickets):
    """Return all stored tickets as a list."""
    return list(tickets.values())
