---
doc_type: feature_design
feature_id: F-002
status: design_draft
last_updated: 2026-03-05
---
# COMMIT Command Design

## Architecture

The COMMIT command orchestrates the `Workspace` (F-001) and `LLMClient` layers to create structured checkpoints of agent progress.

```
src/gitmem/
├── commands/
│   └── commit.py     # commit() async function
├── llm.py            # LLMClient.summarize_for_commit()
└── prompts.py        # COMMIT_PROMPT template
```

## Interfaces / Contracts

```python
async def commit(
    workspace: Workspace,
    llm: LLMClient,
    history: str,
    message: str | None = None,
) -> CommitEntry
```

Flow:
1. `workspace.read_head()` → current branch name
2. `workspace.read_commits(branch)` → existing commits (for sequential ID + context)
3. If `message` is provided, use it directly; otherwise call `llm.summarize_for_commit(history, branch_purpose, prior_commits)`
4. Build `CommitEntry` with next sequential ID (`C-{n+1:03d}`)
5. `workspace.append_commit(branch, entry)`
6. Return the `CommitEntry`

```python
class LLMClient:
    def __init__(self, model: str = "claude-sonnet-4-20250514") -> None
    async def summarize_for_commit(
        self, history: str, branch_purpose: str, prior_commits: str
    ) -> dict  # keys: summary, progress, current_state, next_steps
```

## Data Model

Uses `CommitEntry` from F-001 `models.py`.

## Error Handling

- If LLM call fails and no manual `message` is provided, raise `LLMError` with the underlying exception.
- If workspace is not initialized, the `Workspace` layer raises `WorkspaceNotInitializedError`.

## Testing Strategy

- Mock `LLMClient` to test commit logic without real API calls.
- Test sequential ID assignment with 0, 1, and N existing commits.
- Test manual message bypass path.

## Requirement Mapping

- D-F002-001: `commit()` reads HEAD to determine current branch. Implements R-F002-001.
- D-F002-002: `LLMClient.summarize_for_commit()` calls Anthropic API with structured prompt. Implements R-F002-002.
- D-F002-003: `commit()` parses LLM response into `CommitEntry` model. Implements R-F002-003.
- D-F002-004: Sequential ID assignment via `len(existing_commits) + 1`. Implements R-F002-004.
- D-F002-005: `workspace.append_commit()` persists the entry. Implements R-F002-005.
- D-F002-006: `message` parameter bypasses LLM call. Implements R-F002-006.
- D-F002-007: `commit()` returns the `CommitEntry`. Implements R-F002-007.
