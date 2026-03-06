---
doc_type: feature_verification
feature_id: F-005
status: requirements_draft
last_updated: 2026-03-05
---
# CONTEXT Command Verification

- S-F005-001: Given `main.md` contains roadmap text When `context(resolution="low")` is called Then the roadmap content is returned.
Evidence: S-F005-001 -> tests/test_context.py::test_context_low_resolution

- S-F005-002: Given the current branch has 3 commits When `context(resolution="medium")` is called Then all 3 commit summaries are returned.
Evidence: S-F005-002 -> tests/test_context.py::test_context_medium_resolution

- S-F005-003: Given the current branch's `log.md` has traces When `context(resolution="high")` is called Then the full log is returned.
Evidence: S-F005-003 -> tests/test_context.py::test_context_high_resolution

- S-F005-004: Given commits mention "auth" and "database" When `context(query="auth")` is called Then only auth entries are returned.
Evidence: S-F005-004 -> tests/test_context.py::test_context_query_filter

- S-F005-005: Given no parameters When `context()` is called Then defaults to `resolution="medium"`.
Evidence: S-F005-005 -> tests/test_context.py::test_context_default_resolution
