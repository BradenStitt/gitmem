---
doc_type: feature_tasks
feature_id: F-004
status: tasks_draft
last_updated: 2026-03-05
---
# MERGE Command Tasks

- [ ] T-F004-001 Implement `MERGE_PROMPT` template in `prompts.py` for LLM synthesis (R: R-F004-002, D: D-F004-002)
- [ ] T-F004-002 Implement `LLMClient.synthesize_for_merge()` async method (R: R-F004-002, D: D-F004-002)
- [ ] T-F004-003 Implement `merge()` function with commit reading, LLM synthesis, commit append, roadmap update, and metadata update (R: R-F004-001, R-F004-003, R-F004-004, R-F004-005, R-F004-006, D: D-F004-001, D-F004-003, D-F004-004, D-F004-005, D-F004-006)
- [ ] T-F004-004 Implement source branch validation in `merge()` (R: R-F004-007, D: D-F004-007)
- [ ] T-F004-005 Write unit tests for merge with mocked LLM, default target, roadmap update, and error cases (R: R-F004-001 through R-F004-007, D: D-F004-001 through D-F004-007)
