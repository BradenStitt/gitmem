---
doc_type: feature_verification
feature_id: F-002
status: requirements_draft
last_updated: 2026-03-05
---
# COMMIT Command Verification

- S-F002-001: Given an initialized workspace on branch `main` When `commit(history="Implemented auth module")` is called Then a `CommitEntry` with ID `C-001` is appended and returned.
Evidence: S-F002-001 -> tests/test_commit.py::test_commit_creates_entry

- S-F002-002: Given a branch with two existing commits When `commit()` is called Then the new commit receives ID `C-003`.
Evidence: S-F002-002 -> tests/test_commit.py::test_commit_sequential_id

- S-F002-003: Given a `message` parameter is provided When `commit()` is called Then the commit uses the message without calling the LLM.
Evidence: S-F002-003 -> tests/test_commit.py::test_commit_manual_message

- S-F002-004: Given the LLM call fails When `commit()` is called without a manual message Then the system raises an error.
Evidence: S-F002-004 -> tests/test_commit.py::test_commit_llm_failure
