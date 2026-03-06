---
doc_type: feature_requirements
feature_id: F-004
name: MERGE Command
status: requirements_draft
owner: bradenstitt
last_updated: 2026-03-05
---
# MERGE Command Requirements

## Requirements (EARS + RFC)

- R-F004-001: WHEN `merge(source, target)` is called the system MUST read the commit logs from both the source and target branches.
- R-F004-002: WHEN synthesizing the merge the system MUST call the Anthropic LLM to produce a unified summary integrating insights from the source branch into the target branch.
- R-F004-003: WHEN the LLM synthesis is complete the system MUST append a new commit entry to the target branch's `commit.md` containing the merged summary.
- R-F004-004: WHEN the merge results in roadmap changes the system MUST update `main.md` to reflect the new project state.
- R-F004-005: WHEN the merge completes successfully the system MUST update the source branch's `metadata.yaml` status to `merged`.
- R-F004-006: IF no `target` parameter is provided THEN the system MUST default to the current branch (from `HEAD`).
- R-F004-007: WHEN `merge()` is called with a source branch that does not exist the system MUST raise an error.

## Acceptance Scenarios (Gherkin)

- S-F004-001: Given branches `main` and `experiment` exist with commits on both When `merge("experiment", "main")` is called Then a new commit is appended to `main`'s `commit.md` containing synthesized content from `experiment`, and `experiment`'s metadata status is set to `merged`.
- S-F004-002: Given `HEAD` points to `main` When `merge("experiment")` is called without a target Then the merge targets `main`.
- S-F004-003: Given only branch `main` exists When `merge("nonexistent")` is called Then the system raises an error.
- S-F004-004: Given a merge produces roadmap insights When `merge()` completes Then `main.md` is updated with the new project state.
