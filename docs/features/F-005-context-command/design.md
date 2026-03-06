---
doc_type: feature_design
feature_id: F-005
status: design_draft
last_updated: 2026-03-05
---
# CONTEXT Command Design

## Architecture

Pure-filesystem retrieval with optional keyword filtering. No LLM calls.

```
src/gitmem/commands/
└── context.py    # context() function
```

## Interfaces / Contracts

```python
def context(
    workspace: Workspace,
    resolution: str = "medium",
    query: str | None = None,
) -> ContextResult
```

Flow:
1. Read HEAD to get current branch.
2. Based on `resolution`:
   - `"low"`: `workspace.read_main()` → content, source = `"main.md"`
   - `"medium"`: `workspace.read_commits(branch)` → format commits as text, source = `"branches/<branch>/commit.md"`
   - `"high"`: `workspace.read_log(branch)` → content, source = `"branches/<branch>/log.md"`
3. If `query` is provided, filter content to lines containing query (case-insensitive).
4. Return `ContextResult(resolution, content, source)`.

## Data Model

Uses `ContextResult` from F-001 `models.py`.

## Error Handling

- Invalid `resolution` value raises `ValueError`.
- Empty/missing files return `ContextResult` with empty `content` string (R-F005-006).

## Testing Strategy

- Test each resolution level returns correct source file content.
- Test query filtering with matching and non-matching terms.
- Test default resolution.
- Test empty file handling.

## Requirement Mapping

- D-F005-001: `resolution="low"` reads `main.md`. Implements R-F005-001.
- D-F005-002: `resolution="medium"` reads `commit.md`. Implements R-F005-002.
- D-F005-003: `resolution="high"` reads `log.md`. Implements R-F005-003.
- D-F005-004: `query` parameter filters content case-insensitively. Implements R-F005-004.
- D-F005-005: Default `resolution` is `"medium"`. Implements R-F005-005.
- D-F005-006: Empty/missing files return empty `ContextResult`. Implements R-F005-006.
