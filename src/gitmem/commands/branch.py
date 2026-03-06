"""BRANCH and CHECKOUT commands (F-003)."""

from __future__ import annotations

from datetime import UTC, datetime

from gitmem.errors import BranchExistsError, BranchNotFoundError
from gitmem.models import BranchMetadata
from gitmem.workspace import Workspace


def branch(workspace: Workspace, name: str, purpose: str) -> BranchMetadata:
    """Create a new branch from the current branch and switch to it."""
    if workspace.branch_exists(name):
        raise BranchExistsError(f"Branch '{name}' already exists")

    current = workspace.read_head()

    # Create branch directory with empty commit.md and log.md
    workspace.create_branch_dir(name)

    # Copy last commit from current branch (if any)
    commits = workspace.read_commits(current)
    if commits:
        workspace.append_commit(name, commits[-1])

    # Write metadata
    now = datetime.now(UTC)
    meta = BranchMetadata(
        name=name,
        parent=current,
        purpose=purpose,
        created_at=now,
        status="active",
    )
    workspace.write_metadata(name, meta)

    # Switch HEAD
    workspace.write_head(name)

    return meta


def checkout(workspace: Workspace, name: str) -> None:
    """Switch HEAD to an existing branch."""
    if not workspace.branch_exists(name):
        raise BranchNotFoundError(f"Branch '{name}' does not exist")
    workspace.write_head(name)
