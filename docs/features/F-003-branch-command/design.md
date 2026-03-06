---
doc_type: feature_design
feature_id: F-003
status: design_draft
last_updated: 2026-03-05
---
# BRANCH Command Design

## Architecture

Pure-filesystem operations via `Workspace`. No LLM calls needed.

```
src/gitmem/commands/
└── branch.py    # branch() and checkout() functions
```

## Interfaces / Contracts

```python
def branch(workspace: Workspace, name: str, purpose: str) -> BranchMetadata
def checkout(workspace: Workspace, name: str) -> None
```

`branch()` flow:
1. Check `workspace.branch_exists(name)` — raise `BranchExistsError` if true.
2. `workspace.read_head()` → current branch.
3. `workspace.read_commits(current_branch)` → get last commit.
4. `workspace.create_branch_dir(name)` → create directory.
5. If last commit exists, `workspace.append_commit(name, last_commit)`.
6. Build `BranchMetadata(name, parent=current_branch, purpose, created_at=now, status="active")`.
7. `workspace.write_metadata(name, metadata)`.
8. `workspace.write_head(name)` → switch to new branch.
9. Return the `BranchMetadata`.

`checkout()` flow:
1. Check `workspace.branch_exists(name)` — raise `BranchNotFoundError` if false.
2. `workspace.write_head(name)`.

## Data Model

Uses `BranchMetadata` from F-001 `models.py`.

## Error Handling

- `BranchExistsError` when creating a branch that already exists (R-F003-005).
- `BranchNotFoundError` when checking out a non-existent branch (R-F003-007).

## Testing Strategy

- Test branch creation with and without existing commits.
- Test HEAD update after branch and checkout.
- Test error cases for duplicate branch names and missing branches.

## Requirement Mapping

- D-F003-001: `branch()` creates directory via `workspace.create_branch_dir()`. Implements R-F003-001.
- D-F003-002: `branch()` copies last commit from current branch. Implements R-F003-002.
- D-F003-003: `branch()` writes metadata with parent, purpose, timestamp, status. Implements R-F003-003.
- D-F003-004: `branch()` updates HEAD to new branch. Implements R-F003-004.
- D-F003-005: `branch()` checks `branch_exists()` and raises error. Implements R-F003-005.
- D-F003-006: `checkout()` updates HEAD to target branch. Implements R-F003-006.
- D-F003-007: `checkout()` checks `branch_exists()` and raises error. Implements R-F003-007.
