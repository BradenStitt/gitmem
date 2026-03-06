"""Tests for MCP server (F-006)."""

from __future__ import annotations

import pytest

from gitmem_mcp.server import (
    _instances,
    gitmem_branch,
    gitmem_checkout,
    gitmem_context,
    gitmem_init,
    gitmem_log,
)


@pytest.fixture(autouse=True)
def clear_instances():
    _instances.clear()
    yield
    _instances.clear()


# --- S-F006-001: tools are registered ---


@pytest.mark.asyncio
async def test_all_tools_registered():
    from gitmem_mcp.server import mcp

    tools = await mcp.list_tools()
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


# --- S-F006-002: init tool ---


def test_gitmem_init_tool(tmp_path):
    result = gitmem_init(root=str(tmp_path))
    assert "initialized" in result.lower()
    assert (tmp_path / ".gitmem").is_dir()


# --- S-F006-004: error handling ---


def test_error_handling_init(tmp_path):
    # Init twice should return error string, not crash
    gitmem_init(root=str(tmp_path))
    result = gitmem_init(root=str(tmp_path))
    assert result.startswith("Error:")


def test_checkout_error(tmp_path):
    gitmem_init(root=str(tmp_path))
    result = gitmem_checkout(branch="nonexistent", root=str(tmp_path))
    assert result.startswith("Error:")


# --- Branch + context integration ---


def test_branch_and_context(tmp_path):
    root = str(tmp_path)
    gitmem_init(root=root)

    result = gitmem_branch(name="feature", purpose="Test feature", root=root)
    assert "feature" in result

    result = gitmem_context(resolution="low", root=root)
    assert "Roadmap" in result


# --- Log tool ---


def test_log_tool(tmp_path):
    root = str(tmp_path)
    gitmem_init(root=root)
    result = gitmem_log(entry="Agent executed step 1", root=root)
    assert "appended" in result.lower()
