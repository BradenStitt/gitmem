---
doc_type: feature_verification
feature_id: F-004
status: requirements_draft
last_updated: 2026-03-05
---
# MERGE Command Verification

- S-F004-001: Given branches `main` and `experiment` with commits When `merge("experiment", "main")` is called Then a merge commit is appended to `main` and `experiment` status is set to `merged`.
Evidence: S-F004-001 -> tests/test_merge.py::test_merge_creates_commit_and_updates_status

- S-F004-002: Given `HEAD` points to `main` When `merge("experiment")` is called without target Then the merge targets `main`.
Evidence: S-F004-002 -> tests/test_merge.py::test_merge_default_target

- S-F004-003: Given only branch `main` exists When `merge("nonexistent")` is called Then the system raises an error.
Evidence: S-F004-003 -> tests/test_merge.py::test_merge_nonexistent_source_raises

- S-F004-004: Given a merge produces roadmap insights When `merge()` completes Then `main.md` is updated.
Evidence: S-F004-004 -> tests/test_merge.py::test_merge_updates_roadmap
