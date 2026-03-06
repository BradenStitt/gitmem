"""MCP protocol-level integration tests using FastMCP Client.

These tests verify the MCP server works correctly when accessed through
the actual MCP protocol, not just by calling Python functions directly.
"""

from __future__ import annotations

import pytest
from fastmcp import Client

from gitmem_mcp.server import _instances, mcp


@pytest.fixture(autouse=True)
def clear_instances():
    _instances.clear()
    yield
    _instances.clear()


@pytest.mark.asyncio
async def test_init_via_mcp(tmp_path):
    """Test gitmem_init through MCP protocol."""
    async with Client(mcp) as client:
        result = await client.call_tool("gitmem_init", {"root": str(tmp_path)})
        text = result.content[0].text
        assert "initialized" in text.lower()
        assert (tmp_path / ".gitmem").is_dir()


@pytest.mark.asyncio
async def test_full_workflow_via_mcp(tmp_path):
    """Test init -> log -> commit (manual) -> branch -> checkout -> context via MCP."""
    root = str(tmp_path)

    async with Client(mcp) as client:
        # Init
        result = await client.call_tool("gitmem_init", {"root": root})
        assert "initialized" in result.content[0].text.lower()

        # Log
        result = await client.call_tool(
            "gitmem_log", {"entry": "Started working on auth", "root": root}
        )
        assert "appended" in result.content[0].text.lower()

        # Commit (manual message — no LLM needed)
        result = await client.call_tool(
            "gitmem_commit",
            {"history": "Built auth system", "message": "Auth module complete", "root": root},
        )
        text = result.content[0].text
        assert "C-001" in text
        assert "Auth module complete" in text

        # Branch
        result = await client.call_tool(
            "gitmem_branch",
            {"name": "oauth", "purpose": "Add OAuth support", "root": root},
        )
        assert "oauth" in result.content[0].text

        # Commit on new branch
        result = await client.call_tool(
            "gitmem_commit",
            {
                "history": "Added OAuth provider",
                "message": "OAuth provider integrated",
                "root": root,
            },
        )
        assert "C-002" in result.content[0].text

        # Checkout back to main
        result = await client.call_tool(
            "gitmem_checkout", {"branch": "main", "root": root}
        )
        assert "main" in result.content[0].text

        # Context (low)
        result = await client.call_tool(
            "gitmem_context", {"resolution": "low", "root": root}
        )
        assert "Roadmap" in result.content[0].text

        # Context (medium)
        result = await client.call_tool(
            "gitmem_context", {"resolution": "medium", "root": root}
        )
        assert "Auth module complete" in result.content[0].text

        # Context (high — log)
        result = await client.call_tool(
            "gitmem_context", {"resolution": "high", "root": root}
        )
        assert "auth" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_error_returns_string_not_crash(tmp_path):
    """Test that errors are returned as strings, not exceptions."""
    root = str(tmp_path)

    async with Client(mcp) as client:
        # Checkout without init
        result = await client.call_tool(
            "gitmem_checkout", {"branch": "main", "root": root}
        )
        assert "error" in result.content[0].text.lower()

        # Init then duplicate init
        await client.call_tool("gitmem_init", {"root": root})
        result = await client.call_tool("gitmem_init", {"root": root})
        assert "error" in result.content[0].text.lower()

        # Checkout nonexistent branch
        result = await client.call_tool(
            "gitmem_checkout", {"branch": "nonexistent", "root": root}
        )
        assert "error" in result.content[0].text.lower()


@pytest.mark.asyncio
async def test_tool_listing():
    """Test that all 7 tools are discoverable via MCP protocol."""
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_names = {t.name for t in tools}
        expected = {
            "gitmem_init",
            "gitmem_commit",
            "gitmem_branch",
            "gitmem_merge",
            "gitmem_context",
            "gitmem_checkout",
            "gitmem_log",
        }
        assert expected.issubset(tool_names)


@pytest.mark.asyncio
async def test_tool_parameter_schemas():
    """Test that tools have correct parameter schemas."""
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_map = {t.name: t for t in tools}

        # gitmem_commit should have 'history'
        commit_schema = tool_map["gitmem_commit"].inputSchema
        assert "history" in commit_schema.get("properties", {})

        # gitmem_branch should have 'name' and 'purpose'
        branch_schema = tool_map["gitmem_branch"].inputSchema
        props = branch_schema.get("properties", {})
        assert "name" in props
        assert "purpose" in props

        # gitmem_context should have 'resolution' and 'query'
        context_schema = tool_map["gitmem_context"].inputSchema
        props = context_schema.get("properties", {})
        assert "resolution" in props
        assert "query" in props
