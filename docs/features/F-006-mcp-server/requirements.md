---
doc_type: feature_requirements
feature_id: F-006
name: MCP Server
status: requirements_draft
owner: bradenstitt
last_updated: 2026-03-05
---
# MCP Server Requirements

## Requirements (EARS + RFC)

- R-F006-001: WHEN the MCP server starts the system MUST expose GitMem commands as FastMCP 3.0 tools: `gitmem_init`, `gitmem_commit`, `gitmem_branch`, `gitmem_merge`, `gitmem_context`, `gitmem_checkout`, and `gitmem_log`.
- R-F006-002: WHEN an MCP tool is invoked the system MUST delegate to the corresponding function in the `gitmem` Python package.
- R-F006-003: WHEN an MCP tool encounters an error from the core package the system MUST return a structured error message to the caller without crashing the server.
- R-F006-004: WHEN `gitmem_init` is called the system MUST accept an optional `root` parameter specifying the workspace path, defaulting to the current working directory.
- R-F006-005: WHEN `gitmem_commit` is called the system MUST accept `history` (required) and `message` (optional) parameters.
- R-F006-006: WHEN `gitmem_branch` is called the system MUST accept `name` (required) and `purpose` (required) parameters.
- R-F006-007: WHEN `gitmem_context` is called the system MUST accept `resolution` (optional, default `medium`) and `query` (optional) parameters.

## Acceptance Scenarios (Gherkin)

- S-F006-001: Given the MCP server is running When a client lists available tools Then all 7 GitMem tools are returned with their parameter schemas.
- S-F006-002: Given the MCP server is running When `gitmem_init` is invoked with `root="/tmp/test"` Then a `.gitmem/` workspace is created at `/tmp/test/.gitmem/`.
- S-F006-003: Given the MCP server is running and a workspace exists When `gitmem_commit` is invoked with `history="did work"` Then a commit is created and its summary is returned as text.
- S-F006-004: Given the core package raises an error When any MCP tool is invoked Then the server returns the error message without crashing.
