---
doc_type: steering
version: 2.0.0
last_reviewed: 2026-03-05
---
# Steering

## Product Constraints

- Python 3.11+ required.
- Tooling: uv (package management), ruff (linting/formatting).
- LLM calls use the Anthropic Python SDK exclusively.
- Default summarization model: `claude-sonnet-4-20250514` (configurable).
- Workspace directory name: `.gitmem/` (not `.GCC/`).
- All workspace files are plain text (Markdown + YAML) — no binary formats.
- Async interface for LLM-calling commands (commit, merge); sync for pure-filesystem commands (branch, checkout, context, log).

## Design Principles

- **Git-inspired, not Git-dependent**: Mirror Git semantics conceptually but do not depend on or shell out to Git.
- **Append-only commits**: Commit logs are never rewritten, only appended.
- **Human-readable workspace**: All `.gitmem/` files should be inspectable by humans.
- **Minimal dependencies**: Core package depends only on `anthropic`, `pydantic`, and `pyyaml`.
- **Separation of concerns**: Workspace I/O, LLM integration, and command logic are distinct layers.
- **MCP server wraps the Python API**: The MCP server is a thin layer over the core package, not a separate implementation.
