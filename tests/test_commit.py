"""Tests for COMMIT command (F-002)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from gitmem.commands.commit import commit
from gitmem.llm import LLMClient, LLMError
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
            "summary": "Implemented feature X",
            "progress": "Feature X complete",
            "current_state": "Ready for testing",
            "next_steps": ["Write tests", "Deploy"],
        }
    )
    return llm


# --- S-F002-001: commit creates entry ---


@pytest.mark.asyncio
async def test_commit_creates_entry(ws, mock_llm):
    entry = await commit(ws, mock_llm, history="Implemented auth module")
    assert entry.id == "C-001"
    assert entry.summary == "Implemented feature X"
    assert entry.branch == "main"

    # Verify persisted
    commits = ws.read_commits("main")
    assert len(commits) == 1
    assert commits[0].id == "C-001"


# --- S-F002-002: sequential IDs ---


@pytest.mark.asyncio
async def test_commit_sequential_id(ws, mock_llm):
    await commit(ws, mock_llm, history="First")
    await commit(ws, mock_llm, history="Second")
    entry = await commit(ws, mock_llm, history="Third")
    assert entry.id == "C-003"


# --- S-F002-003: manual message bypass ---


@pytest.mark.asyncio
async def test_commit_manual_message(ws, mock_llm):
    entry = await commit(ws, mock_llm, history="work", message="Manual checkpoint")
    assert entry.summary == "Manual checkpoint"
    mock_llm.summarize_for_commit.assert_not_called()


# --- S-F002-004: LLM failure ---


@pytest.mark.asyncio
async def test_commit_llm_failure(ws):
    llm = LLMClient.__new__(LLMClient)
    llm.summarize_for_commit = AsyncMock(side_effect=LLMError("API failed"))
    with pytest.raises(LLMError):
        await commit(ws, llm, history="work")
