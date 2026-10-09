def make_ticket(
    ticket_id="T001",
    *,
    title="Campus Wi-Fi is down",
    category="Network",
    urgency="high",
    affected_users=15,
    priority="critical",
    status="open",
    assigned_to=None,
):
    """Return a fresh ticket dictionary for use in unit tests."""
    return {
        "id": ticket_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }
