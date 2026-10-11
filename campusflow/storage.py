import json
from pathlib import Path


def save_tickets(tickets, file_path):
    """Save ticket records to a JSON file.

    Args:
        tickets (dict): Tickets keyed by ticket ID.
        file_path (str or Path): Destination file path.
    """
    if not isinstance(tickets, dict):
        raise TypeError("Tickets must be a dictionary.")

    path = Path(file_path)

    # Create the parent directory if it does not exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)
    except (OSError, TypeError, ValueError) as error:
        raise ValueError(
            f"Could not save tickets to '{path}': {error}"
        ) from error


def load_tickets(file_path):
    """Load ticket records from a JSON file.

    Returns an empty dictionary if the file does not exist.

    Raises:
        ValueError: If the file contains invalid JSON.
    """
    path = Path(file_path)

    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in '{path}': {error}"
        ) from error
    except OSError as error:
        raise ValueError(
            f"Could not read tickets from '{path}': {error}"
        ) from error

    if not isinstance(tickets, dict):
        raise ValueError(
            f"Invalid ticket data in '{path}': "
            "expected a JSON object keyed by ticket ID."
        )

    return tickets