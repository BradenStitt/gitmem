"""MERGE command (F-004)."""

from __future__ import annotations

from datetime import UTC, datetime

from gitmem.errors import BranchNotFoundError
from gitmem.llm import LLMClient
from gitmem.models import CommitEntry
from gitmem.workspace import Workspace


async def merge(
    workspace: Workspace,
    llm: LLMClient,
    source: str,
    target: str | None = None,
) -> str:
    """Merge insights from source branch into target branch via LLM synthesis."""
    if target is None:
        target = workspace.read_head()

    if not workspace.branch_exists(source):
        raise BranchNotFoundError(f"Source branch '{source}' does not exist")

    source_commits = workspace.read_commits(source)
    target_commits = workspace.read_commits(target)
    roadmap = workspace.read_main()

    source_text = "\n".join(f"- {c.id}: {c.summary}" for c in source_commits) or "(no commits)"
    target_text = "\n".join(f"- {c.id}: {c.summary}" for c in target_commits) or "(no commits)"

    data = await llm.synthesize_for_merge(
        source_commits=source_text,
        target_commits=target_text,
        roadmap=roadmap,
    )

    # Create merge commit on target
    existing_target = workspace.read_commits(target)
    next_id = f"C-{len(existing_target) + 1:03d}"
    now = datetime.now(UTC)

    entry = CommitEntry(
        id=next_id,
        timestamp=now,
        branch=target,
        summary=data["summary"],
        progress=data["progress"],
        current_state=data["current_state"],
        next_steps=data.get("next_steps", []),
    )
    workspace.append_commit(target, entry)

    # Update roadmap if needed
    roadmap_update = data.get("roadmap_update")
    if roadmap_update:
        workspace.write_main(roadmap_update)

    # Mark source as merged
    source_meta = workspace.read_metadata(source)
    source_meta.status = "merged"
    workspace.write_metadata(source, source_meta)

    return data["summary"]
