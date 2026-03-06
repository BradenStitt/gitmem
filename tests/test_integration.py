"""End-to-end integration test exercising the full GitMem lifecycle.

Covers the complete workflow: init → log → commit → branch → commit →
checkout → merge → context at all resolutions.

Uses mocked LLM to avoid real API calls while testing the full pipeline.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from gitmem import GitMem
from gitmem.llm import LLMClient


@pytest.fixture
def gm(tmp_path):
    """Return a GitMem instance with mocked LLM at a temp directory."""
    gm = GitMem(root=tmp_path)

    # Replace the LLM with a mock
    mock_llm = LLMClient.__new__(LLMClient)
    mock_llm.summarize_for_commit = AsyncMock(
        return_value={
            "summary": "Implemented core feature",
            "progress": "Core feature complete",
            "current_state": "Feature functional",
            "next_steps": ["Add tests", "Write docs"],
        }
    )
    mock_llm.synthesize_for_merge = AsyncMock(
        return_value={
            "summary": "Merged experiment results into main",
            "progress": "Experiment integrated",
            "current_state": "Main branch updated with experiment findings",
            "next_steps": ["Deploy", "Monitor"],
            "roadmap_update": "# Project Roadmap\n\nPhase 1 complete. Moving to deployment.",
        }
    )
    gm.llm = mock_llm
    return gm


@pytest.mark.asyncio
async def test_full_lifecycle(gm):
    """Test the complete GitMem workflow end-to-end."""
    # 1. Initialize workspace
    gm.init()
    assert gm.workspace.read_head() == "main"
    assert gm.workspace.list_branches() == ["main"]

    # 2. Log some work on main
    gm.log("Started project setup")
    gm.log("Created initial file structure")
    log_content = gm.workspace.read_log("main")
    assert "project setup" in log_content
    assert "file structure" in log_content

    # 3. Commit on main (with LLM)
    entry1 = await gm.commit(history="Set up project, created models and workspace")
    assert entry1.id == "C-001"
    assert entry1.branch == "main"
    assert entry1.summary == "Implemented core feature"

    # 4. Create a branch
    meta = gm.branch("experiment", "Try alternative algorithm")
    assert meta.name == "experiment"
    assert meta.parent == "main"
    assert meta.status == "active"
    assert gm.workspace.read_head() == "experiment"

    # Verify the last commit was copied to the new branch
    exp_commits = gm.workspace.read_commits("experiment")
    assert len(exp_commits) == 1
    assert exp_commits[0].id == "C-001"

    # 5. Do work and commit on experiment branch
    gm.log("Trying approach A")
    gm.log("Approach A shows promise")
    entry2 = await gm.commit(history="Tried approach A, looks promising")
    assert entry2.id == "C-002"
    assert entry2.branch == "experiment"

    # 6. Manual commit (no LLM)
    entry3 = await gm.commit(
        history="n/a", message="Checkpoint: approach A benchmarked"
    )
    assert entry3.id == "C-003"
    assert entry3.summary == "Checkpoint: approach A benchmarked"

    # 7. Switch back to main
    gm.checkout("main")
    assert gm.workspace.read_head() == "main"

    # Main should still have only 1 commit
    main_commits = gm.workspace.read_commits("main")
    assert len(main_commits) == 1

    # 8. Merge experiment into main
    summary = await gm.merge(source="experiment")
    assert "Merged experiment" in summary

    # Main now has 2 commits (original + merge)
    main_commits = gm.workspace.read_commits("main")
    assert len(main_commits) == 2
    assert main_commits[1].summary == "Merged experiment results into main"

    # Experiment branch should be marked as merged
    exp_meta = gm.workspace.read_metadata("experiment")
    assert exp_meta.status == "merged"

    # Roadmap should be updated
    roadmap = gm.workspace.read_main()
    assert "Phase 1 complete" in roadmap

    # 9. Context at all resolutions
    ctx_low = gm.context(resolution="low")
    assert ctx_low.resolution == "low"
    assert "Phase 1 complete" in ctx_low.content
    assert ctx_low.source == "main.md"

    ctx_med = gm.context(resolution="medium")
    assert ctx_med.resolution == "medium"
    assert "C-001" in ctx_med.content
    assert "C-002" in ctx_med.content
    assert ctx_med.source == "branches/main/commit.md"

    ctx_high = gm.context(resolution="high")
    assert ctx_high.resolution == "high"
    assert ctx_high.source == "branches/main/log.md"

    # 10. Context with query filter
    ctx_filtered = gm.context(resolution="medium", query="Merged")
    assert "Merged" in ctx_filtered.content

    # 11. Verify branches list
    branches = gm.workspace.list_branches()
    assert "main" in branches
    assert "experiment" in branches


@pytest.mark.asyncio
async def test_multi_branch_workflow(gm):
    """Test creating multiple branches and merging sequentially."""
    gm.init()

    # Commit baseline
    await gm.commit(history="baseline", message="Initial baseline")

    # Create two branches from main
    gm.branch("feature-a", "Add feature A")
    await gm.commit(history="feature a work", message="Feature A done")
    gm.checkout("main")

    gm.branch("feature-b", "Add feature B")
    await gm.commit(history="feature b work", message="Feature B done")
    gm.checkout("main")

    # Merge both back
    await gm.merge(source="feature-a")
    await gm.merge(source="feature-b")

    main_commits = gm.workspace.read_commits("main")
    # 1 baseline + 2 merges = 3
    assert len(main_commits) == 3

    assert gm.workspace.read_metadata("feature-a").status == "merged"
    assert gm.workspace.read_metadata("feature-b").status == "merged"


@pytest.mark.asyncio
async def test_workspace_persists_across_instances(tmp_path):
    """Test that workspace state persists when creating a new GitMem instance."""
    # Instance 1: init and commit
    gm1 = GitMem(root=tmp_path)
    mock_llm = LLMClient.__new__(LLMClient)
    mock_llm.summarize_for_commit = AsyncMock(
        return_value={
            "summary": "First session work",
            "progress": "Progress",
            "current_state": "State",
            "next_steps": [],
        }
    )
    gm1.llm = mock_llm
    gm1.init()
    await gm1.commit(history="session 1 work")

    # Instance 2: should see existing state
    gm2 = GitMem(root=tmp_path)
    commits = gm2.workspace.read_commits("main")
    assert len(commits) == 1
    assert commits[0].summary == "First session work"

    ctx = gm2.context(resolution="medium")
    assert "First session work" in ctx.content
