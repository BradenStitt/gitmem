"""FastMCP 3.0 server exposing GitMem commands as MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from gitmem import GitMem

mcp = FastMCP("gitmem")

# Cache GitMem instances by root path
_instances: dict[str, GitMem] = {}


def _get_gitmem(root: str = ".") -> GitMem:
    if root not in _instances:
        _instances[root] = GitMem(root=root)
    return _instances[root]


@mcp.tool
def gitmem_init(root: str = ".") -> str:
    """Initialize a new .gitmem/ workspace."""
    try:
        gm = _get_gitmem(root)
        gm.init()
        return f"Workspace initialized at {root}/.gitmem/"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
async def gitmem_commit(history: str, message: str | None = None, root: str = ".") -> str:
    """Create a structured checkpoint of agent progress."""
    try:
        gm = _get_gitmem(root)
        entry = await gm.commit(history, message)
        return f"Commit {entry.id}: {entry.summary}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
def gitmem_branch(name: str, purpose: str, root: str = ".") -> str:
    """Create a new branch and switch to it."""
    try:
        gm = _get_gitmem(root)
        meta = gm.branch(name, purpose)
        return f"Created branch '{meta.name}' from '{meta.parent}'"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
async def gitmem_merge(source: str, target: str | None = None, root: str = ".") -> str:
    """Merge insights from source branch into target branch."""
    try:
        gm = _get_gitmem(root)
        summary = await gm.merge(source, target)
        return f"Merged: {summary}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
def gitmem_context(
    resolution: str = "medium", query: str | None = None, root: str = "."
) -> str:
    """Retrieve memory context at the specified resolution level."""
    try:
        gm = _get_gitmem(root)
        result = gm.context(resolution, query)
        return result.content or "(empty)"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
def gitmem_checkout(branch: str, root: str = ".") -> str:
    """Switch to an existing branch."""
    try:
        gm = _get_gitmem(root)
        gm.checkout(branch)
        return f"Switched to branch '{branch}'"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
def gitmem_log(entry: str, root: str = ".") -> str:
    """Append an execution trace entry to the current branch log."""
    try:
        gm = _get_gitmem(root)
        gm.log(entry)
        return "Log entry appended"
    except Exception as e:
        return f"Error: {e}"
