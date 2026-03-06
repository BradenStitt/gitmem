"""COMMIT command (F-002)."""

from __future__ import annotations

from datetime import UTC, datetime

from gitmem.llm import LLMClient
from gitmem.models import CommitEntry
from gitmem.workspace import Workspace


async def commit(
    workspace: Workspace,
    llm: LLMClient,
    history: str,
    message: str | None = None,
) -> CommitEntry:
    """Create a structured checkpoint of agent progress on the current branch."""
    branch = workspace.read_head()
    existing = workspace.read_commits(branch)
    next_id = f"C-{len(existing) + 1:03d}"
    now = datetime.now(UTC)

    if message:
        # Manual message bypass — no LLM call
        data = {
            "summary": message,
            "progress": message,
            "current_state": message,
            "next_steps": [],
        }
    else:
        # LLM summarization
        meta = workspace.read_metadata(branch)
        prior = "\n".join(f"- {c.id}: {c.summary}" for c in existing) if existing else ""
        data = await llm.summarize_for_commit(
            history=history,
            branch_purpose=meta.purpose,
            prior_commits=prior,
        )

    entry = CommitEntry(
        id=next_id,
        timestamp=now,
        branch=branch,
        summary=data["summary"],
        progress=data["progress"],
        current_state=data["current_state"],
        next_steps=data.get("next_steps", []),
    )

    workspace.append_commit(branch, entry)
    return entry
