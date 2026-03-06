---
doc_type: feature_requirements
feature_id: F-003
name: BRANCH Command
status: requirements_draft
owner: bradenstitt
last_updated: 2026-03-05
---
# BRANCH Command Requirements

## Requirements (EARS + RFC)

- R-F003-001: WHEN `branch(name, purpose)` is called the system MUST create a new directory under `branches/` with the given name.
- R-F003-002: WHEN a branch is created the system MUST copy the last commit entry from the current branch's `commit.md` to the new branch's `commit.md`.
- R-F003-003: WHEN a branch is created the system MUST write a `metadata.yaml` file recording the branch `name`, `parent` (current branch), `purpose`, `created_at` timestamp, and `status` as `active`.
- R-F003-004: WHEN a branch is created the system MUST update the `HEAD` file to point to the new branch.
- R-F003-005: WHEN `branch()` is called with a name that already exists the system MUST raise an error without modifying any files.
- R-F003-006: WHEN `checkout(name)` is called with an existing branch name the system MUST update the `HEAD` file to point to that branch.
- R-F003-007: WHEN `checkout()` is called with a non-existent branch name the system MUST raise an error.

## Acceptance Scenarios (Gherkin)

- S-F003-001: Given the workspace is on branch `main` with one commit When `branch("experiment", "Try alternative parser")` is called Then `branches/experiment/` is created with `commit.md` containing the last commit from `main`, `metadata.yaml` with parent `main`, and `HEAD` now reads `experiment`.
- S-F003-002: Given branch `experiment` already exists When `branch("experiment", "duplicate")` is called Then the system raises an error and no files are modified.
- S-F003-003: Given branches `main` and `experiment` exist When `checkout("main")` is called Then `HEAD` is updated to `main`.
- S-F003-004: Given only branch `main` exists When `checkout("nonexistent")` is called Then the system raises an error.
