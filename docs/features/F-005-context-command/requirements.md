---
doc_type: feature_requirements
feature_id: F-005
name: CONTEXT Command
status: requirements_draft
owner: bradenstitt
last_updated: 2026-03-05
---
# CONTEXT Command Requirements

## Requirements (EARS + RFC)

- R-F005-001: WHEN `context(resolution="low")` is called the system MUST return the content of `main.md` (global project roadmap).
- R-F005-002: WHEN `context(resolution="medium")` is called the system MUST return the commit summaries from the current branch's `commit.md`.
- R-F005-003: WHEN `context(resolution="high")` is called the system MUST return the detailed execution traces from the current branch's `log.md`.
- R-F005-004: IF a `query` parameter is provided THEN the system MUST filter returned content to lines or entries containing the query string (case-insensitive).
- R-F005-005: WHEN `context()` is called without a `resolution` parameter the system MUST default to `medium`.
- R-F005-006: WHEN the requested file is empty or does not exist the system MUST return an empty `ContextResult` with appropriate metadata.

## Acceptance Scenarios (Gherkin)

- S-F005-001: Given `main.md` contains roadmap text When `context(resolution="low")` is called Then the system returns a `ContextResult` with the roadmap content and `source` set to `main.md`.
- S-F005-002: Given the current branch has 3 commits When `context(resolution="medium")` is called Then the system returns all 3 commit summaries.
- S-F005-003: Given the current branch's `log.md` has OTA traces When `context(resolution="high")` is called Then the system returns the full log content.
- S-F005-004: Given commit summaries mention "auth" and "database" When `context(resolution="medium", query="auth")` is called Then only entries containing "auth" are returned.
- S-F005-005: Given no parameters are provided When `context()` is called Then the system defaults to `resolution="medium"`.
