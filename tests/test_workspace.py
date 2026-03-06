"""Tests for the Workspace file system layer (F-001)."""

from datetime import UTC, datetime

import pytest

from gitmem.errors import (
    BranchNotFoundError,
    WorkspaceExistsError,
    WorkspaceNotInitializedError,
)
from gitmem.models import BranchMetadata, CommitEntry
from gitmem.workspace import Workspace


@pytest.fixture
def ws(tmp_path):
    """Return an initialized Workspace rooted at a temp directory."""
    w = Workspace(tmp_path)
    w.init()
    return w


# --- S-F001-001: init creates full structure ---


def test_init_creates_structure(tmp_path):
    ws = Workspace(tmp_path)
    ws.init()

    gitmem = tmp_path / ".gitmem"
    assert gitmem.is_dir()
    assert (gitmem / "HEAD").read_text().strip() == "main"
    assert (gitmem / "main.md").exists()
    assert (gitmem / "branches" / "main" / "commit.md").exists()
    assert (gitmem / "branches" / "main" / "log.md").exists()
    assert (gitmem / "branches" / "main" / "metadata.yaml").exists()


# --- S-F001-002: init raises on existing ---


def test_init_raises_on_existing(ws):
    with pytest.raises(WorkspaceExistsError):
        ws.init()


# --- S-F001-003: read_head returns main ---


def test_read_head_default(ws):
    assert ws.read_head() == "main"


# --- HEAD write/read round-trip ---


def test_write_and_read_head(ws):
    ws.write_head("experiment")
    assert ws.read_head() == "experiment"


# --- Uninitialized workspace raises ---


def test_uninitialized_raises(tmp_path):
    ws = Workspace(tmp_path)
    with pytest.raises(WorkspaceNotInitializedError):
        ws.read_head()


# --- S-F001-004: list_branches ---


def test_list_branches_default(ws):
    assert ws.list_branches() == ["main"]


def test_list_branches_multiple(ws):
    ws.create_branch_dir("experiment")
    branches = ws.list_branches()
    assert branches == ["experiment", "main"]


# --- branch_exists ---


def test_branch_exists(ws):
    assert ws.branch_exists("main") is True
    assert ws.branch_exists("nonexistent") is False


# --- create_branch_dir ---


def test_create_branch_dir(ws):
    ws.create_branch_dir("feature")
    assert ws.branch_exists("feature")
    branch_dir = ws.gitmem_dir / "branches" / "feature"
    assert (branch_dir / "commit.md").exists()
    assert (branch_dir / "log.md").exists()


# --- main.md read/write ---


def test_read_main_default(ws):
    content = ws.read_main()
    assert "Roadmap" in content


def test_write_and_read_main(ws):
    ws.write_main("# Updated Roadmap\n\nNew content.")
    assert ws.read_main() == "# Updated Roadmap\n\nNew content."


# --- Metadata read/write ---


def test_metadata_round_trip(ws):
    meta = ws.read_metadata("main")
    assert meta.name == "main"
    assert meta.parent is None
    assert meta.status == "active"


def test_write_and_read_metadata(ws):
    now = datetime.now(UTC)
    meta = BranchMetadata(
        name="experiment",
        parent="main",
        purpose="Test new approach",
        created_at=now,
        status="active",
    )
    ws.create_branch_dir("experiment")
    ws.write_metadata("experiment", meta)
    loaded = ws.read_metadata("experiment")
    assert loaded.name == "experiment"
    assert loaded.parent == "main"
    assert loaded.purpose == "Test new approach"
    assert loaded.status == "active"


# --- S-F001-005: append_commit and read_commits ---


def test_append_and_read_commits(ws):
    now = datetime.now(UTC)
    entry = CommitEntry(
        id="C-001",
        timestamp=now,
        branch="main",
        summary="Initial work",
        progress="Set up project structure",
        current_state="Scaffolding complete",
        next_steps=["Implement core logic"],
    )
    ws.append_commit("main", entry)
    commits = ws.read_commits("main")
    assert len(commits) == 1
    assert commits[0].id == "C-001"
    assert commits[0].summary == "Initial work"


def test_read_commits_empty(ws):
    assert ws.read_commits("main") == []


def test_append_multiple_commits(ws):
    now = datetime.now(UTC)
    for i in range(3):
        entry = CommitEntry(
            id=f"C-{i + 1:03d}",
            timestamp=now,
            branch="main",
            summary=f"Commit {i + 1}",
            progress=f"Step {i + 1}",
            current_state=f"State {i + 1}",
            next_steps=[f"Next {i + 1}"],
        )
        ws.append_commit("main", entry)
    commits = ws.read_commits("main")
    assert len(commits) == 3
    assert commits[0].id == "C-001"
    assert commits[2].id == "C-003"


# --- Log read/write ---


def test_read_log_empty(ws):
    assert ws.read_log("main") == ""


def test_append_and_read_log(ws):
    ws.append_log("main", "Step 1: Initialized project")
    ws.append_log("main", "Step 2: Created models")
    log = ws.read_log("main")
    assert "Step 1" in log
    assert "Step 2" in log


# --- Error: branch not found ---


def test_branch_not_found_metadata(ws):
    with pytest.raises(BranchNotFoundError):
        ws.read_metadata("nonexistent")


def test_branch_not_found_commits(ws):
    with pytest.raises(BranchNotFoundError):
        ws.read_commits("nonexistent")
