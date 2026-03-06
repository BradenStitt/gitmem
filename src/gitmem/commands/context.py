"""CONTEXT command (F-005)."""

from __future__ import annotations

from gitmem.models import ContextResult
from gitmem.workspace import Workspace


def context(
    workspace: Workspace,
    resolution: str = "medium",
    query: str | None = None,
) -> ContextResult:
    """Retrieve memory context at the specified resolution level."""
    branch = workspace.read_head()

    if resolution == "low":
        content = workspace.read_main()
        source = "main.md"
    elif resolution == "medium":
        commits = workspace.read_commits(branch)
        content = "\n\n".join(
            f"## {c.id} ({c.timestamp.isoformat()})\n{c.summary}\n\n"
            f"**Progress:** {c.progress}\n"
            f"**State:** {c.current_state}\n"
            f"**Next:** {', '.join(c.next_steps)}"
            for c in commits
        )
        source = f"branches/{branch}/commit.md"
    elif resolution == "high":
        content = workspace.read_log(branch)
        source = f"branches/{branch}/log.md"
    else:
        raise ValueError(f"Invalid resolution: {resolution!r}. Must be low, medium, or high.")

    if query:
        query_lower = query.lower()
        lines = content.splitlines()
        content = "\n".join(line for line in lines if query_lower in line.lower())

    return ContextResult(resolution=resolution, content=content, source=source)
