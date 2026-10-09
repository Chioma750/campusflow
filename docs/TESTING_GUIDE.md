# CampusFlow Testing Guide

## 1. Install and activate Python

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version
```

Use Python 3.12 for the shared development environment.

## 2. Run the full test suite

```bash
python -m unittest discover -s tests -v
```

`unittest` is built into Python; no test package installation is required.

## 3. Run one test module

```bash
python -m unittest tests.test_tickets -v
python -m unittest tests.test_workflow -v
python -m unittest tests.test_reports -v
python -m unittest tests.test_storage -v
```

## 4. Understand expected initial failures

These are test-first specifications. If the application functions have not
been implemented yet, test discovery may report import errors because modules
or functions are missing. That is expected at this stage. Once the modules
exist, failing assertions identify behavior that still needs implementation.

## 5. Implement one vertical slice at a time

Recommended sequence:

1. Developer A implements `create_ticket()` and its tests.
2. Developer A implements `get_ticket()` and `list_tickets()`.
3. Developer B implements `assign_ticket()`.
4. Developer B implements `update_status()`.
5. Developer B implements `get_work_queue()`.
6. Developer B implements `generate_report()`.
7. Developer A implements `save_tickets()` and `load_tickets()`.
8. Both developers integrate the CLI and run the complete suite.

For each slice:
- Read the matching tests first.
- Implement only the required behavior.
- Run the relevant test module.
- Run the full suite.
- Inspect `git diff`.
- Commit a focused change on a feature branch.
- Push and open a pull request.

## 6. GitHub Actions

The workflow at `.github/workflows/tests.yml` runs the same test command on
pushes to `main` and pull requests targeting `main`.

After pushing the workflow:
1. Open the repository's Actions tab.
2. Open the `CampusFlow Tests` workflow run.
3. Check the test output.
4. Fix failures on the feature branch and push again.

The workflow will fail until all imported modules/functions exist and the
tests pass. Do not disable the workflow just to obtain a green check.

## 7. Temporary files

Storage tests use temporary directories and clean them up automatically.
They should not read from or overwrite a developer's real runtime data file.
