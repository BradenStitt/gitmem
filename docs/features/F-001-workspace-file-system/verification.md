---
doc_type: feature_verification
feature_id: F-001
status: requirements_draft
last_updated: 2026-03-05
---
# Workspace File System Verification

- S-F001-001: Given no `.gitmem/` directory exists When `init()` is called Then the system creates the full workspace structure.
Evidence: S-F001-001 -> tests/test_workspace.py::test_init_creates_structure

- S-F001-002: Given a `.gitmem/` directory already exists When `init()` is called Then the system raises an error.
Evidence: S-F001-002 -> tests/test_workspace.py::test_init_raises_on_existing

- S-F001-003: Given an initialized workspace When `read_head()` is called Then the system returns `main`.
Evidence: S-F001-003 -> tests/test_workspace.py::test_read_head_default

- S-F001-004: Given branches `main` and `experiment` When `list_branches()` is called Then returns sorted list.
Evidence: S-F001-004 -> tests/test_workspace.py::test_list_branches

- S-F001-005: Given an initialized workspace When `append_commit()` is called Then entry is persisted and retrievable.
Evidence: S-F001-005 -> tests/test_workspace.py::test_append_and_read_commits
