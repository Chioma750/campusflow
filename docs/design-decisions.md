# CampusFlow: Summary of Design Decisions Between Developer A and Developer B

## 1. Project Architecture

CampusFlow was designed as a modular Python command-line application for managing campus technical support requests. The team agreed to separate business logic into dedicated modules rather than place all functionality in one file.

The architecture consists of `tickets.py`, `workflow.py`, `storage.py`, `reports.py`, and `main.py`, with automated tests in a separate `tests/` directory. The CLI acts as the integration layer, coordinating the modules while keeping business rules separate from user interaction.

## 2. Division of Responsibilities

Responsibilities were divided by functional requirements to reduce conflicts and establish clear ownership.

- Developer A: F1 — ticket creation, validation, ID generation, and priority calculation; F2 — ticket listing and detail viewing; F7 — JSON persistence.
- Developer B: F3 — ticket assignment; F4 — status workflow; F5 — prioritized work queue; F6 — reports and statistics.

Although responsibilities were divided, both developers must follow the shared interfaces and ticket data contract.

## 3. Shared Ticket Data Contract

Tickets are represented as Python dictionaries containing eight fields: `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, and `assigned_to`.

Ticket IDs follow the `T001`, `T002`, and subsequent numbering pattern. Categories are `Network`, `Hardware`, `Software`, and `Other`; urgency levels are `low`, `medium`, and `high`.

The team chose this common structure so that assignment, workflow, reporting, persistence, and CLI integration could operate on the same ticket records without incompatible representations.

## 4. Business Rules

The team established consistent rules across modules:

- Priority is calculated using urgency and the number of affected users, with critical issues taking precedence.
- Tickets progress through `open`, `in_progress`, and `resolved`.
- Unassigned tickets cannot enter `in_progress`.
- Resolved tickets must be explicitly reopened before modification.
- The work queue excludes resolved tickets and sorts by priority, then numeric ticket ID.
- Reports calculate totals and status and priority breakdowns dynamically, including when no tickets exist.

## 5. Persistence and Testing

JSON was selected for local persistence, with runtime data stored separately from source code. The `data/` directory is excluded through `.gitignore`.

The team uses Python's built-in `unittest` framework. Developers must test their changes and run the complete suite using:

`python -m unittest discover -s tests -v`

The CLI integration work subsequently passed 47 automated tests.

## 6. Git and Collaboration

The agreed workflow uses issue-linked feature branches, focused commits, pull requests, review, and testing before merging into `main`. Developers should preserve each other's work and avoid duplicating functionality already implemented on another branch.

PR #12 provides the CLI integration layer. Other feature branches and pull requests must be checked for dependencies and overlapping changes before merging.

Overall decision: CampusFlow prioritizes modularity, a shared data contract, explicit workflow rules, automated verification, and controlled integration through GitHub pull requests.
