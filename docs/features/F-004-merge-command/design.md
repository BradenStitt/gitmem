---
doc_type: feature_design
feature_id: F-004
status: design_draft
last_updated: 2026-03-05
---
# MERGE Command Design

## Architecture

Orchestrates `Workspace` and `LLMClient` to synthesize divergent reasoning paths.

```
src/gitmem/
├── commands/
│   └── merge.py      # merge() async function
├── llm.py            # LLMClient.synthesize_for_merge()
└── prompts.py        # MERGE_PROMPT template
```

## Interfaces / Contracts

```python
async def merge(
    workspace: Workspace,
    llm: LLMClient,
    source: str,
    target: str | None = None,
) -> str  # returns the merge summary
```

Flow:
1. If `target` is None, read HEAD as target (R-F004-006).
2. Validate `workspace.branch_exists(source)` — raise error if not (R-F004-007).
3. `workspace.read_commits(source)` → source commits.
4. `workspace.read_commits(target)` → target commits.
5. `workspace.read_main()` → current roadmap.
6. Call `llm.synthesize_for_merge(source_commits, target_commits, roadmap)`.
7. Build `CommitEntry` for the merge, append to target branch.
8. If LLM indicates roadmap updates, `workspace.write_main(updated_roadmap)` (R-F004-004).
9. Update source metadata status to `merged` (R-F004-005).
10. Return merge summary.

```python
class LLMClient:
    async def synthesize_for_merge(
        self, source_commits: str, target_commits: str, roadmap: str
    ) -> dict  # keys: summary, roadmap_update (optional)
```

## Data Model

Uses `CommitEntry` and `BranchMetadata` from F-001.

## Error Handling

- `BranchNotFoundError` when source branch does not exist.
- `LLMError` if the synthesis call fails.

## Testing Strategy

- Mock LLM to test merge orchestration.
- Test default target from HEAD.
- Test roadmap update path vs. no-update path.
- Test source branch metadata status update.

## Requirement Mapping

- D-F004-001: `merge()` reads commits from both branches. Implements R-F004-001.
- D-F004-002: `LLMClient.synthesize_for_merge()` calls Anthropic API. Implements R-F004-002.
- D-F004-003: `merge()` appends synthesis as commit to target. Implements R-F004-003.
- D-F004-004: `merge()` updates `main.md` when roadmap changes. Implements R-F004-004.
- D-F004-005: `merge()` sets source metadata status to `merged`. Implements R-F004-005.
- D-F004-006: `merge()` defaults target to HEAD. Implements R-F004-006.
- D-F004-007: `merge()` validates source branch existence. Implements R-F004-007.
