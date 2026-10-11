
def generate_report(tickets):
    """Generate ticket totals grouped by status and priority."""

    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
    }

    for ticket in tickets.values():
        status = ticket["status"]
        priority = ticket["priority"]

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report
