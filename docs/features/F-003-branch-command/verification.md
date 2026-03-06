---
doc_type: feature_verification
feature_id: F-003
status: requirements_draft
last_updated: 2026-03-05
---
# BRANCH Command Verification

- S-F003-001: Given the workspace is on branch `main` with one commit When `branch("experiment", "Try alternative parser")` is called Then the new branch is created with copied commit, metadata, and HEAD updated.
Evidence: S-F003-001 -> tests/test_branch.py::test_branch_creates_with_commit_copy

- S-F003-002: Given branch `experiment` already exists When `branch("experiment", "duplicate")` is called Then the system raises an error.
Evidence: S-F003-002 -> tests/test_branch.py::test_branch_duplicate_raises

- S-F003-003: Given branches `main` and `experiment` exist When `checkout("main")` is called Then `HEAD` is updated to `main`.
Evidence: S-F003-003 -> tests/test_branch.py::test_checkout_switches_head

- S-F003-004: Given only branch `main` exists When `checkout("nonexistent")` is called Then the system raises an error.
Evidence: S-F003-004 -> tests/test_branch.py::test_checkout_nonexistent_raises
