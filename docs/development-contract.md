# CampusFlow Development Contract

This document defines the initial function interfaces expected by the tests.
The team should agree to this contract before implementing features. If an
interface changes, update its tests and notify the other developer.

## Shared ticket collection

The application keeps tickets in a dictionary keyed by ticket ID:

```python
tickets = {
    "T001": {
        "id": "T001",
        "title": "Campus Wi-Fi is down",
        "category": "Network",
        "urgency": "high",
        "affected_users": 15,
        "priority": "critical",
        "status": "open",
        "assigned_to": None,
    }
}
```

## `campusflow.tickets` — Developer A

- `create_ticket(tickets, title, category, urgency, affected_users)`
  validates input, calculates priority, creates and stores a ticket, and
  returns the created ticket dictionary.
- `get_ticket(tickets, ticket_id)` returns the ticket or raises `KeyError`.
- `list_tickets(tickets)` returns a list of ticket dictionaries.

Valid categories: `Network`, `Hardware`, `Software`, `Other`.
Valid urgency values: `low`, `medium`, `high`.
Valid priority values: `critical`, `high`, `medium`, `low`.
New tickets start with status `open` and `assigned_to` set to `None`.
IDs are `T001`, `T002`, etc., and must remain unique after persistence reload.

Priority rules, evaluated in this order:
1. urgency is high and affected_users >= 10: critical
2. urgency is high or affected_users >= 10: high
3. urgency is medium or affected_users >= 3: medium
4. otherwise: low

Invalid input raises `ValueError` and must not mutate the collection.

## `campusflow.workflow` — Developer B

- `assign_ticket(tickets, ticket_id, staff_name)` assigns and returns the ticket.
- `update_status(tickets, ticket_id, new_status)` changes status and returns
  the ticket.
- `get_work_queue(tickets)` returns a list of unresolved tickets ordered by
  priority (`critical`, `high`, `medium`, `low`) and then by numeric ticket ID.

Unknown IDs raise `KeyError`; invalid operations raise `ValueError` without
mutating ticket data.

Status transitions:
- `open` -> `in_progress` only when assigned.
- `in_progress` -> `resolved`.
- `resolved` -> `open` to explicitly reopen.
- Other transitions are rejected.

A resolved ticket cannot be assigned/reassigned. After reopening, normal
assignment and workflow rules apply again.

## `campusflow.reports` — Developer B

`generate_report(tickets)` returns:

```python
{
    "total": 0,
    "by_status": {"open": 0, "in_progress": 0, "resolved": 0},
    "by_priority": {
        "critical": 0, "high": 0, "medium": 0, "low": 0
    },
}
```

All categories are included even when their counts are zero.

## `campusflow.storage` — Developer A

- `save_tickets(tickets, file_path)` writes a JSON object keyed by ticket ID.
- `load_tickets(file_path)` returns that dictionary.
- A missing file returns `{}`.
- Malformed JSON raises a clear `ValueError`; do not silently replace bad data
  with an empty collection.

## Test convention

Run all tests with:

```bash
python -m unittest discover -s tests -v
```

Tests use only the Python standard library.
