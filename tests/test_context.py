"""Tests for CONTEXT command (F-005)."""

from datetime import UTC, datetime

import pytest

from gitmem.commands.context import context
from gitmem.models import CommitEntry
from gitmem.workspace import Workspace


@pytest.fixture
def ws(tmp_path):
    w = Workspace(tmp_path)
    w.init()
    return w


def _make_commit(ws, cid, summary, branch="main"):
    now = datetime.now(UTC)
    entry = CommitEntry(
        id=cid,
        timestamp=now,
        branch=branch,
        summary=summary,
        progress="progress",
        current_state="state",
        next_steps=["next"],
    )
    ws.append_commit(branch, entry)


# --- S-F005-001: low resolution returns main.md ---


def test_context_low_resolution(ws):
    ws.write_main("# My Roadmap\n\nGoals here.")
    result = context(ws, resolution="low")
    assert result.resolution == "low"
    assert "My Roadmap" in result.content
    assert result.source == "main.md"


# --- S-F005-002: medium resolution returns commits ---


def test_context_medium_resolution(ws):
    _make_commit(ws, "C-001", "Built auth module")
    _make_commit(ws, "C-002", "Added database layer")
    _make_commit(ws, "C-003", "Wrote tests")

    result = context(ws, resolution="medium")
    assert result.resolution == "medium"
    assert "C-001" in result.content
    assert "C-002" in result.content
    assert "C-003" in result.content
    assert result.source == "branches/main/commit.md"


# --- S-F005-003: high resolution returns log ---


def test_context_high_resolution(ws):
    ws.append_log("main", "Step 1: Ran diagnostics")
    ws.append_log("main", "Step 2: Fixed issue")

    result = context(ws, resolution="high")
    assert result.resolution == "high"
    assert "Step 1" in result.content
    assert "Step 2" in result.content
    assert result.source == "branches/main/log.md"


# --- S-F005-004: query filtering ---


def test_context_query_filter(ws):
    _make_commit(ws, "C-001", "Built auth module")
    _make_commit(ws, "C-002", "Added database layer")

    result = context(ws, resolution="medium", query="auth")
    assert "auth" in result.content.lower()
    assert "database" not in result.content.lower()


# --- S-F005-005: default resolution ---


def test_context_default_resolution(ws):
    result = context(ws)
    assert result.resolution == "medium"


# --- Empty content ---


def test_context_medium_empty(ws):
    result = context(ws, resolution="medium")
    assert result.content == ""


def test_context_high_empty(ws):
    result = context(ws, resolution="high")
    assert result.content == ""


# --- Invalid resolution ---


def test_context_invalid_resolution(ws):
    with pytest.raises(ValueError):
        context(ws, resolution="ultra")
