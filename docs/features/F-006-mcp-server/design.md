---
doc_type: feature_design
feature_id: F-006
status: design_draft
last_updated: 2026-03-05
---
# MCP Server Design

## Architecture

Thin FastMCP 3.0 wrapper over the `gitmem` Python package. Separate package namespace `gitmem_mcp`.

```
src/gitmem_mcp/
├── __init__.py
└── server.py    # FastMCP server with @mcp.tool decorators
```

## Interfaces / Contracts

Each MCP tool maps 1:1 to a `gitmem` function:

| MCP Tool | Core Function | Async |
|----------|--------------|-------|
| `gitmem_init` | `GitMem.init()` | No |
| `gitmem_commit` | `GitMem.commit()` | Yes |
| `gitmem_branch` | `GitMem.branch()` | No |
| `gitmem_merge` | `GitMem.merge()` | Yes |
| `gitmem_context` | `GitMem.context()` | No |
| `gitmem_checkout` | `GitMem.checkout()` | No |
| `gitmem_log` | `GitMem.log()` | No |

The server instantiates a `GitMem` instance per `root` parameter. For simplicity, a single default instance is used when no root is specified.

## Error Handling

All tool functions wrap core calls in try/except and return error strings to the MCP client rather than raising exceptions (R-F006-003).

## Security / Privacy

- No authentication in initial implementation (local use only).
- Root path is validated to prevent path traversal.

## Testing Strategy

- Test that all tools are registered and have correct parameter schemas.
- Test error propagation from core package to MCP response.
- Integration test with FastMCP test client.

## Requirement Mapping

- D-F006-001: All 7 tools registered via `@mcp.tool` decorators. Implements R-F006-001.
- D-F006-002: Each tool delegates to corresponding `GitMem` method. Implements R-F006-002.
- D-F006-003: Try/except wrapping returns error strings. Implements R-F006-003.
- D-F006-004: `gitmem_init` accepts optional `root` parameter. Implements R-F006-004.
- D-F006-005: `gitmem_commit` accepts `history` and `message`. Implements R-F006-005.
- D-F006-006: `gitmem_branch` accepts `name` and `purpose`. Implements R-F006-006.
- D-F006-007: `gitmem_context` accepts `resolution` and `query`. Implements R-F006-007.
