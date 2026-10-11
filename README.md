# CampusFlow — Campus Technical Support Ticket Manager

**A Python CLI application for managing campus technical support requests.**

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-unittest-success)](https://docs.python.org/3/library/unittest.html)
[![Interface](https://img.shields.io/badge/Interface-CLI-orange)]()

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Project Objectives](#project-objectives)
- [Features](#features)
- [Ticket Data Model](#ticket-data-model)
- [Priority Calculation](#priority-calculation)
- [Ticket Lifecycle](#ticket-lifecycle)
- [Work Queue](#work-queue)
- [Reports](#reports)
- [Data Persistence](#data-persistence)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [Example Ticket](#example-ticket)
- [Design Principles](#design-principles)
- [Development Workflow](#development-workflow)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview

CampusFlow is a command-line ticket management system developed to help campus support teams record, organize, prioritize, assign, and resolve technical support requests.

The application is designed for a Learn2Earn campus environment where staff and learners may encounter technical problems that affect their ability to access learning resources and perform their daily activities.

CampusFlow provides a structured alternative to informal reporting methods by keeping support requests in a centralized ticket collection, tracking their status, assigning responsibility, and preserving ticket data between application sessions.

The project is built with Python using a modular architecture and automated tests.

## Problem Statement

Campus technical support requests can include:

- Campus Wi-Fi outages.
- Faulty laptops and computer hardware.
- Broken development environments.
- Inaccessible learning platforms.
- Software configuration problems.
- Other technical issues affecting campus activities.

When these problems are reported informally, important requests can be overlooked, responsibility may be unclear, and urgent issues may not receive attention promptly.

CampusFlow addresses these challenges by providing a consistent workflow for recording requests, determining their priority, assigning staff members, tracking progress, and generating summary reports.

## Project Objectives

The primary objectives are to:

1. Provide a consistent way to create and validate support tickets.
2. Assign unique identifiers to individual tickets.
3. Calculate ticket priority using urgency and the number of affected users.
4. Allow support staff to list and inspect tickets.
5. Assign responsibility for resolving reported problems.
6. Enforce valid ticket status transitions.
7. Present unresolved tickets in priority order.
8. Generate useful ticket statistics.
9. Persist ticket data in JSON format.
10. Maintain code quality through modular design and automated testing.

## Features

CampusFlow is organized around seven core functional requirements.

### F1 — Ticket Creation and Validation

Users can create tickets by providing the relevant information about a technical problem.

The system:

- Validates required input fields.
- Rejects blank ticket titles.
- Validates ticket categories and urgency levels.
- Requires the number of affected users to be a positive integer.
- Calculates priority automatically.
- Generates a unique ticket identifier.
- Initializes the ticket status as `open`.
- Initializes the assignee as `None`.

### F2 — Ticket Listing and Detail Viewing

Users can:

- Display all existing tickets.
- View the details of an individual ticket using its identifier.
- Inspect information such as title, category, urgency, priority, status, affected users, and assigned staff member.
- Receive appropriate feedback when a requested ticket does not exist.

### F3 — Ticket Assignment

Tickets can be assigned to staff members responsible for resolving them.

Assignment rules include:

- The ticket must exist.
- The staff member's name must not be empty or consist only of whitespace.
- A resolved ticket cannot be reassigned until it is explicitly reopened.

### F4 — Ticket Workflow Management

CampusFlow tracks the progress of tickets through the following lifecycle:

`open → in_progress → resolved`

The workflow enforces these rules:

- A ticket must be assigned before it can move to `in_progress`.
- A ticket can progress through valid status transitions.
- A resolved ticket cannot be modified until it is explicitly reopened.
- Reopening a resolved ticket changes its status to `open`, allowing further work.

These restrictions help maintain consistent ticket state and prevent invalid operations.

### F5 — Prioritized Work Queue

The work queue displays open, unresolved tickets in priority order.

Priority ranking:

1. Critical
2. High
3. Medium
4. Low

When two tickets have the same priority, the ticket with the earlier numeric identifier is listed first.

Resolved tickets are excluded from the active work queue.

### F6 — Reports and Statistics

CampusFlow generates a report containing:

- The total number of tickets.
- The number of tickets in each status.
- The number of tickets at each priority level.

Reports must also work when no tickets exist, returning zero counts rather than failing.

### F7 — Data Persistence

CampusFlow saves ticket records to a JSON file so they can be loaded during a subsequent application session.

The persistence functionality supports:

- Saving the ticket collection.
- Loading previously saved tickets.
- Continuing work across application restarts.
- Initial startup when no saved data file exists.
- Appropriate handling of invalid or malformed saved data.

The application's runtime data is stored separately from the source code.

## Ticket Data Model

Tickets are represented as Python dictionaries.

Each ticket contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique ticket identifier, such as `T001` |
| `title` | Short description of the technical problem |
| `category` | Type of technical issue |
| `urgency` | Reported urgency level |
| `affected_users` | Positive integer representing the number of affected users |
| `priority` | Automatically calculated priority |
| `status` | Current workflow state |
| `assigned_to` | Assigned staff member, or `None` if unassigned |

### Allowed values

**Categories**

- `Network`
- `Hardware`
- `Software`
- `Other`

**Urgency levels**

- `low`
- `medium`
- `high`

**Priority levels**

- `low`
- `medium`
- `high`
- `critical`

**Ticket statuses**

- `open`
- `in_progress`
- `resolved`

Inputs should be validated and normalized consistently so that acceptable case variations do not produce inconsistent records.

## Priority Calculation

Ticket priority is calculated from urgency and the number of affected users.

The rules are evaluated in the following order:

| Condition | Priority |
|---|---|
| Urgency is `high` and at least 10 users are affected | `critical` |
| Urgency is `high`, or at least 10 users are affected | `high` |
| Urgency is `medium`, or at least 3 users are affected | `medium` |
| None of the above conditions apply | `low` |

The order is important because a ticket may satisfy more than one condition.

For example, a high-urgency network outage affecting 15 users should receive `critical` priority rather than merely `high`.

This approach helps the support team prioritize issues according to urgency and impact.

## Ticket Lifecycle

The ticket lifecycle controls how a support request progresses from creation to resolution.

### 1. Open

A newly created ticket begins with:

- Status: `open`
- Assigned staff member: `None`

The ticket is recorded and awaits assignment or further action.

### 2. In Progress

Once a staff member has been assigned, the ticket can move to `in_progress`.

This indicates that work has started.

### 3. Resolved

After the problem has been addressed, the ticket can move to `resolved`.

Resolved tickets are excluded from the active work queue.

### 4. Reopening a Resolved Ticket

If further work becomes necessary, the ticket must first be explicitly reopened.

Reopening changes its status to `open`. This allows the ticket to re-enter the active workflow.

The system does not permit a resolved ticket to be modified as though it were still active.

## Work Queue

The work queue helps support staff determine which outstanding requests should receive attention first.

Tickets are ordered by:

1. Priority, from `critical` to `low`.
2. Numeric ticket identifier, ascending, when priorities are equal.

Only open, unresolved tickets are included.

For example, if `T002` and `T005` are both high priority, `T002` appears first.

This provides a predictable ordering and ensures that higher-impact problems are visible before lower-priority requests.

## Reports

The reporting module summarizes the current ticket collection.

A report includes the total number of tickets and breakdowns by status and priority.

For example, a report could indicate that a collection contains 10 tickets, with 4 open, 3 in progress, and 3 resolved.

The numbers above are illustrative; actual reports are calculated from the ticket data.

When the collection is empty, all totals and breakdowns should return zero.

## Data Persistence

CampusFlow uses JSON for local data persistence.

The CLI integration uses the following runtime data path:

`data/tickets.json`

The application loads saved tickets at startup and saves the collection when the user exits through the application menu.

The `data/` directory is excluded through `.gitignore` so runtime ticket records are not accidentally committed to the source repository.

**Important:** JSON persistence is intended for this project's local CLI workflow. It is not a substitute for a production database or a multi-user synchronization system.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13+ | Application implementation |
| Python dictionaries | In-memory ticket representation |
| JSON | Local ticket persistence |
| `pathlib` | File and directory path management |
| `unittest` | Automated testing |
| Git | Version control |
| GitHub | Repository hosting, issues, and pull requests |

The core application uses Python's standard library and does not require a third-party package installation for its documented test workflow.

## Project Structure

The project follows a modular structure that separates ticket operations, workflow rules, persistence, reporting, and the CLI.

```text
campusflow/
├── main.py
├── README.md
├── .gitignore
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
├── tests/
│   ├── helpers.py
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   ├── test_reports.py
│   └── test_main.py
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

The exact files may evolve as development continues.

### Module responsibilities

**`main.py`**

Provides the command-line interface, menu, user input handling, application-level error handling, and coordination between modules.

**`campusflow/tickets.py`**

Handles ticket validation, unique identifier generation, priority calculation, ticket creation, listing, and retrieval.

**`campusflow/workflow.py`**

Implements ticket assignment, status transitions, reopening rules, and work queue generation.

**`campusflow/storage.py`**

Handles saving and loading ticket collections using JSON.

**`campusflow/reports.py`**

Calculates ticket totals and breakdowns by status and priority.

**`tests/`**

Contains automated tests for module behavior and application integration.

**`docs/`**

Contains project learning notes and design decisions.

## Getting Started

### Prerequisites

- Python 3.13 or a compatible supported Python version.
- Git.
- A terminal or command-line environment.
- The CampusFlow repository.

### 1. Clone the repository

```bash
git clone https://github.com/Chioma750/campusflow.git
cd campusflow
```

### 2. Verify your Python version

```bash
python --version
```

On systems where Python is invoked through `python3`, use:

```bash
python3 --version
```

### 3. Verify the project files

Ensure the repository contains `main.py`, the `campusflow/` package, and the `tests/` directory.

No separate package installation is required for the standard-library-based application and test commands described here.

## Running the Application

From the project root, run:

```bash
python main.py
```

The application presents a menu for interacting with the ticket manager.

The intended menu operations include:

1. Create a ticket.
2. List all tickets.
3. View a ticket by ID.
4. Assign a ticket.
5. Update ticket status.
6. View the prioritized work queue.
7. Generate reports.
0. Save and exit.

Follow the prompts to perform the desired operation.

Use the application's exit option to save the current ticket collection before leaving.

## Running Tests

CampusFlow uses Python's built-in `unittest` framework.

Run the complete test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The test suite covers ticket operations, workflow rules, persistence, reporting, validation, and CLI integration.

The CLI integration work has previously passed a run of **47 automated tests**. Run the command above against your current checkout to verify its present state; the test count may change as the project evolves.

Tests should be rerun after changes to ticket rules, module interfaces, persistence, or application integration.

## Example Ticket

The following JSON illustrates the structure of a ticket record:

```json
{
  "id": "T001",
  "title": "Campus Wi-Fi is down",
  "category": "Network",
  "urgency": "high",
  "affected_users": 15,
  "priority": "critical",
  "status": "open",
  "assigned_to": null
}
```

In Python, the corresponding dictionary uses `None` for the unassigned staff member:

```python
ticket = {
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": None,
}
```

JSON represents Python's `None` as `null` when the record is serialized.

The example is illustrative; actual ticket records are created and managed by the application.

## Design Principles

CampusFlow follows these engineering principles:

### Separation of concerns

Each module is responsible for a specific area of functionality. This makes the application easier to understand, test, and maintain.

### Input validation

User input is validated before it is used to create or modify ticket records.

### Consistent business rules

Priority calculation, ticket assignment, and status transitions are governed by explicit rules rather than duplicated across the application.

### Predictable behavior

Ticket identifiers, work queue ordering, and error handling should produce consistent results.

### Persistence

Ticket data should remain available between application sessions when successfully saved.

### Testability

The modules and CLI are covered by automated tests so that changes can be verified without relying exclusively on manual testing.

## Development Workflow

CampusFlow uses Git and GitHub to organize collaborative development.

### Issues

Each feature or task should be tracked through a GitHub Issue with a clear description and acceptance criteria.

### Branches

Create a dedicated branch for a task or feature. A naming convention such as the following is recommended:

```text
feat/2-ticket-listing-and-viewing
feat/3-ticket-assignment
feat/6-ticket-reports
```

Use the repository's agreed branch naming conventions and check existing branches before starting duplicate work.

### Pull requests

Submit changes through pull requests so that code can be reviewed and tested before being merged into `main`.

Where a pull request fully completes a GitHub Issue, link it using a closing keyword such as:

```text
Closes #2
```

GitHub will close the linked issue when the pull request is merged into the default branch.

### Before merging

- Confirm the change meets the issue's acceptance criteria.
- Run the complete automated test suite.
- Review the pull request's files and commits.
- Check for overlapping changes and merge conflicts.
- Ensure required feature dependencies are available in `main`.

Avoid merging a feature solely because its tests pass on an isolated branch; verify it against the integrated application as well.

## Future Improvements

Potential future enhancements include:

- More detailed audit history for ticket assignments and status changes.
- Improved filtering and searching of tickets.
- Exportable reports.
- Additional validation and recovery options for persisted data.
- A database-backed storage layer.
- A web interface or API for broader access.
- Multi-user support with appropriate access control.

These are potential extensions, not claims about functionality currently implemented.

## Contributing

Contributions should follow the project's issue-driven workflow.

1. Review existing issues and pull requests.
2. Confirm the task is not already implemented on another branch.
3. Create a feature branch from the appropriate base.
4. Implement the change and add or update automated tests.
5. Run the complete test suite.
6. Commit the changes with a descriptive message.
7. Push the branch and open a pull request.
8. Address review feedback before merging.

Keep changes focused, preserve existing functionality, and document important design decisions.

## License

No license has been specified in this README. Add a license section once the project maintainers have selected and committed the appropriate license file.

---

**CampusFlow** — Bringing structure, accountability, and priority to campus technical support.
