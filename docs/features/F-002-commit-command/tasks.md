---
doc_type: feature_tasks
feature_id: F-002
status: tasks_draft
last_updated: 2026-03-05
---
# COMMIT Command Tasks

- [ ] T-F002-001 Implement `prompts.py` with `COMMIT_PROMPT` template for LLM summarization (R: R-F002-002, D: D-F002-002)
- [ ] T-F002-002 Implement `LLMClient.__init__()` with Anthropic SDK setup and configurable model (R: R-F002-002, D: D-F002-002)
- [ ] T-F002-003 Implement `LLMClient.summarize_for_commit()` async method (R: R-F002-002, R-F002-003, D: D-F002-002, D-F002-003)
- [ ] T-F002-004 Implement `commit()` function with HEAD read, ID assignment, LLM call, and workspace append (R: R-F002-001, R-F002-004, R-F002-005, R-F002-007, D: D-F002-001, D-F002-004, D-F002-005, D-F002-007)
- [ ] T-F002-005 Implement manual message bypass path in `commit()` (R: R-F002-006, D: D-F002-006)
- [ ] T-F002-006 Write unit tests for commit with mocked LLM, sequential IDs, manual message, and error cases (R: R-F002-001 through R-F002-007, D: D-F002-001 through D-F002-007)
