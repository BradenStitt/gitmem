---
doc_type: feature_requirements
feature_id: F-002
name: COMMIT Command
status: requirements_draft
owner: bradenstitt
last_updated: 2026-03-05
---
# COMMIT Command Requirements

## Requirements (EARS + RFC)

- R-F002-001: WHEN `commit()` is called the system MUST read the current branch from the `HEAD` file.
- R-F002-002: WHEN generating a commit summary the system MUST call the Anthropic LLM with the recent interaction history, branch purpose, and prior commit summaries as context.
- R-F002-003: WHEN the LLM returns a summary the system MUST parse it into a `CommitEntry` model containing `id`, `timestamp`, `branch`, `summary`, `progress`, `current_state`, and `next_steps`.
- R-F002-004: WHEN a `CommitEntry` is created the system MUST assign a unique sequential commit ID within the branch (e.g., `C-001`, `C-002`).
- R-F002-005: WHEN the commit entry is finalized the system MUST append it to the `commit.md` file of the current branch via the `Workspace`.
- R-F002-006: WHEN an optional `message` parameter is provided the system SHOULD include it as the primary summary text, bypassing LLM summarization.
- R-F002-007: WHEN `commit()` completes the system MUST return the created `CommitEntry` to the caller.

## Acceptance Scenarios (Gherkin)

- S-F002-001: Given an initialized workspace on branch `main` When `commit(history="Implemented auth module")` is called Then a `CommitEntry` with ID `C-001` is appended to `branches/main/commit.md` and returned.
- S-F002-002: Given a branch with two existing commits When `commit()` is called Then the new commit receives ID `C-003`.
- S-F002-003: Given a `message` parameter is provided When `commit(history, message="Manual checkpoint")` is called Then the commit summary contains the provided message without calling the LLM.
- S-F002-004: Given the LLM call fails When `commit()` is called without a manual message Then the system raises an appropriate error.
