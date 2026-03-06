---
doc_type: feature_verification
feature_id: F-006
status: requirements_draft
last_updated: 2026-03-05
---
# MCP Server Verification

- S-F006-001: Given the MCP server is running When a client lists tools Then all 7 GitMem tools are returned.
Evidence: S-F006-001 -> tests/test_mcp_server.py::test_all_tools_registered

- S-F006-002: Given the MCP server is running When `gitmem_init` is invoked Then a workspace is created.
Evidence: S-F006-002 -> tests/test_mcp_server.py::test_gitmem_init_tool

- S-F006-003: Given a workspace exists When `gitmem_commit` is invoked Then a commit is created.
Evidence: S-F006-003 -> tests/test_mcp_server.py::test_gitmem_commit_tool

- S-F006-004: Given the core package raises an error When any tool is invoked Then the error is returned without crashing.
Evidence: S-F006-004 -> tests/test_mcp_server.py::test_error_handling
