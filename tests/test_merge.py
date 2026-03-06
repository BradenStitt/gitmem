"""Tests for MERGE command (F-004)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from gitmem.commands.branch import branch
from gitmem.commands.commit import commit
from gitmem.commands.merge import merge
from gitmem.errors import BranchNotFoundError
from gitmem.llm import LLMClient
from gitmem.workspace import Workspace


@pytest.fixture
def ws(tmp_path):
    w = Workspace(tmp_path)
    w.init()
    return w


@pytest.fixture
def mock_llm():
    llm = LLMClient.__new__(LLMClient)
    llm.summarize_for_commit = AsyncMock(
        return_value={
            "summary": "Work done",
            "progress": "Progress made",
            "current_state": "State",
            "next_steps": ["Next"],
        }
    )
    llm.synthesize_for_merge = AsyncMock(
        return_value={
            "summary": "Merged experiment into main",
            "progress": "Combined work",
            "current_state": "Unified state",
            "next_steps": ["Continue"],
            "roadmap_update": None,
        }
    )
    return llm


# --- S-F004-001: merge creates commit and updates status ---


@pytest.mark.asyncio
async def test_merge_creates_commit_and_updates_status(ws, mock_llm):
    # Create commits on main
    await commit(ws, mock_llm, history="main work", message="Main work")

    # Create experiment branch and add a commit
    branch(ws, "experiment", "Try something")
    await commit(ws, mock_llm, history="experiment work", message="Experiment work")

    # Merge experiment into main
    from gitmem.commands.branch import checkout

    checkout(ws, "main")
    summary = await merge(ws, mock_llm, source="experiment", target="main")

    assert summary == "Merged experiment into main"

    # Main should have 2 commits (original + merge)
    main_commits = ws.read_commits("main")
    assert len(main_commits) == 2

    # Source branch should be marked merged
    meta = ws.read_metadata("experiment")
    assert meta.status == "merged"


# --- S-F004-002: default target from HEAD ---


@pytest.mark.asyncio
async def test_merge_default_target(ws, mock_llm):
    await commit(ws, mock_llm, history="main work", message="Main work")
    branch(ws, "experiment", "Test")
    await commit(ws, mock_llm, history="exp work", message="Exp work")

    from gitmem.commands.branch import checkout

    checkout(ws, "main")

    # No explicit target — should use HEAD (main)
    summary = await merge(ws, mock_llm, source="experiment")
    assert summary == "Merged experiment into main"


# --- S-F004-003: nonexistent source raises ---


@pytest.mark.asyncio
async def test_merge_nonexistent_source_raises(ws, mock_llm):
    with pytest.raises(BranchNotFoundError):
        await merge(ws, mock_llm, source="nonexistent")


# --- S-F004-004: roadmap update ---


@pytest.mark.asyncio
async def test_merge_updates_roadmap(ws, mock_llm):
    mock_llm.synthesize_for_merge = AsyncMock(
        return_value={
            "summary": "Merged with roadmap change",
            "progress": "New direction",
            "current_state": "Updated",
            "next_steps": ["New path"],
            "roadmap_update": "# Updated Roadmap\n\nNew direction.",
        }
    )
    await commit(ws, mock_llm, history="work", message="Work")
    branch(ws, "experiment", "Explore")
    await commit(ws, mock_llm, history="exp", message="Exp")

    from gitmem.commands.branch import checkout

    checkout(ws, "main")
    await merge(ws, mock_llm, source="experiment")

    roadmap = ws.read_main()
    assert "Updated Roadmap" in roadmap
