---
doc_type: feature_requirements
feature_id: F-001
name: Workspace File System
status: requirements_draft
owner: bradenstitt
last_updated: 2026-03-05
---
# Workspace File System Requirements

## Requirements (EARS + RFC)

- R-F001-001: WHEN the user calls `init()` the system MUST create a `.gitmem/` directory at the specified root path containing `main.md`, `HEAD`, and a `branches/main/` subdirectory.
- R-F001-002: WHEN the `.gitmem/` directory is initialized the system MUST create `commit.md`, `log.md`, and `metadata.yaml` files within the `branches/main/` directory.
- R-F001-003: WHEN `init()` is called and a `.gitmem/` directory already exists the system MUST raise an error indicating the workspace is already initialized.
- R-F001-004: WHEN the system reads or writes workspace files it MUST use the `Workspace` class as the sole interface for all file I/O operations.
- R-F001-005: WHEN a `HEAD` file is read the system MUST return the name of the current active branch as a plain text string.
- R-F001-006: WHEN a branch directory is listed the system MUST return all branch names that exist under `branches/`.
- R-F001-007: WHEN `main.md` is read the system MUST return the global project roadmap content.
- R-F001-008: WHEN metadata is read for a branch the system MUST return a validated `BranchMetadata` model containing `name`, `parent`, `purpose`, `created_at`, and `status` fields.
- R-F001-009: WHEN a commit entry is appended the system MUST persist it to `commit.md` in the correct branch directory using the `CommitEntry` schema.
- R-F001-010: WHEN a log entry is appended the system MUST append it to `log.md` in the active branch directory.

## Acceptance Scenarios (Gherkin)

- S-F001-001: Given no `.gitmem/` directory exists When `init()` is called Then the system creates the full workspace structure with `main.md`, `HEAD` pointing to `main`, and `branches/main/` with `commit.md`, `log.md`, and `metadata.yaml`.
- S-F001-002: Given a `.gitmem/` directory already exists When `init()` is called Then the system raises an error without modifying existing files.
- S-F001-003: Given an initialized workspace When `read_head()` is called Then the system returns the string `main`.
- S-F001-004: Given an initialized workspace with branches `main` and `experiment` When `list_branches()` is called Then the system returns `["experiment", "main"]` sorted alphabetically.
- S-F001-005: Given an initialized workspace When `append_commit(branch, entry)` is called Then the entry is appended to `branches/<branch>/commit.md` and is retrievable via `read_commits(branch)`.
