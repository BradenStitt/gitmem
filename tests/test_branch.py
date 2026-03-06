"""Tests for BRANCH and CHECKOUT commands (F-003)."""

from datetime import UTC, datetime

import pytest

from gitmem.commands.branch import branch, checkout
from gitmem.errors import BranchExistsError, BranchNotFoundError
from gitmem.models import CommitEntry
from gitmem.workspace import Workspace


@pytest.fixture
def ws(tmp_path):
    w = Workspace(tmp_path)
    w.init()
    return w


# --- S-F003-001: branch creates with commit copy ---


def test_branch_creates_with_commit_copy(ws):
    # Add a commit to main first
    now = datetime.now(UTC)
    entry = CommitEntry(
        id="C-001",
        timestamp=now,
        branch="main",
        summary="Initial work",
        progress="Done",
        current_state="Ready",
        next_steps=["Branch out"],
    )
    ws.append_commit("main", entry)

    meta = branch(ws, "experiment", "Try alternative parser")

    assert meta.name == "experiment"
    assert meta.parent == "main"
    assert meta.purpose == "Try alternative parser"
    assert meta.status == "active"
    assert ws.read_head() == "experiment"

    # Last commit from main should be copied
    commits = ws.read_commits("experiment")
    assert len(commits) == 1
    assert commits[0].id == "C-001"


def test_branch_no_commits(ws):
    """Branch from main with no commits — new branch has no commits."""
    meta = branch(ws, "experiment", "Test")
    assert ws.read_commits("experiment") == []
    assert meta.parent == "main"


# --- S-F003-002: duplicate branch raises ---


def test_branch_duplicate_raises(ws):
    branch(ws, "experiment", "First")
    with pytest.raises(BranchExistsError):
        branch(ws, "experiment", "Duplicate")


# --- S-F003-003: checkout switches HEAD ---


def test_checkout_switches_head(ws):
    branch(ws, "experiment", "Test")
    assert ws.read_head() == "experiment"
    checkout(ws, "main")
    assert ws.read_head() == "main"


# --- S-F003-004: checkout nonexistent raises ---


def test_checkout_nonexistent_raises(ws):
    with pytest.raises(BranchNotFoundError):
        checkout(ws, "nonexistent")
