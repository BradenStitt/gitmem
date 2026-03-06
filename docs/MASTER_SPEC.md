---
doc_type: master_spec
product_name: GitMem
version: 2.0.0
status: active
owners: [bradenstitt]
last_reviewed: 2026-03-05
---
# Master Spec

## Vision

GitMem is a version-controlled memory system for LLM agents, inspired by Git. It transforms ephemeral agent context into a persistent, navigable, and structured memory workspace using Git-like operations (COMMIT, BRANCH, MERGE, CONTEXT). This addresses critical limitations in long-horizon AI tasks: unbounded context growth, context decay, lack of exploratory capacity, and session discontinuity.

## Goals

1. Establish a structured, persistent memory system for LLM agents using a hierarchical file-based workspace (`.gitmem/`).
2. Implement version control semantics (commit, branch, merge) for agent reasoning and progress tracking.
3. Enable tiered context retrieval at varying levels of abstraction (roadmap, commit summaries, execution traces).
4. Deliver as both a Python package (`gitmem`) and an MCP server (FastMCP 3.0).
5. Remain agent-agnostic and model-agnostic — usable with any LLM via the Anthropic SDK for internal summarization.

## Non-Goals

- Vector-based semantic search (future enhancement, not initial scope).
- Manus skill integration (deferred).
- Model fine-tuning or proprietary model engineering.
- Real-time collaboration between multiple agents on the same workspace.

## Key Metrics

- All core commands (init, commit, branch, merge, context, checkout, log) functional with test coverage.
- MCP server exposes all commands as tools.
- Workspace persists across sessions and is human-readable.
