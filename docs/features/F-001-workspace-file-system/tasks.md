---
doc_type: feature_tasks
feature_id: F-001
status: tasks_draft
last_updated: 2026-03-05
---
# Workspace File System Tasks

- [ ] T-F001-001 Create `pyproject.toml` with uv config, dependencies, and ruff settings (R: R-F001-004, D: D-F001-008)
- [ ] T-F001-002 Implement `models.py` with `CommitEntry`, `BranchMetadata`, and `ContextResult` Pydantic models (R: R-F001-008, R-F001-009, D: D-F001-005, D-F001-006)
- [ ] T-F001-003 Implement `templates.py` with default content for `main.md`, `HEAD`, `commit.md`, `log.md`, and `metadata.yaml` (R: R-F001-001, R-F001-002, D: D-F001-001)
- [ ] T-F001-004 Implement `Workspace.__init__()` and `Workspace.init()` to create full `.gitmem/` directory structure (R: R-F001-001, R-F001-002, R-F001-003, D: D-F001-001)
- [ ] T-F001-005 Implement `Workspace.read_head()` and `Workspace.write_head()` (R: R-F001-005, D: D-F001-002)
- [ ] T-F001-006 Implement `Workspace.list_branches()`, `branch_exists()`, and `create_branch_dir()` (R: R-F001-006, D: D-F001-003)
- [ ] T-F001-007 Implement `Workspace.read_main()` and `write_main()` (R: R-F001-007, D: D-F001-004)
- [ ] T-F001-008 Implement `Workspace.read_metadata()` and `write_metadata()` (R: R-F001-008, D: D-F001-005)
- [ ] T-F001-009 Implement `Workspace.read_commits()` and `append_commit()` with CommitEntry serialization (R: R-F001-009, D: D-F001-006)
- [ ] T-F001-010 Implement `Workspace.read_log()` and `append_log()` (R: R-F001-010, D: D-F001-007)
- [ ] T-F001-011 Write unit tests for Workspace init, error cases, and all read/write methods (R: R-F001-001 through R-F001-010, D: D-F001-001 through D-F001-008)
