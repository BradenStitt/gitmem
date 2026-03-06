"""GitMem — version-controlled memory system for LLM agents."""

from __future__ import annotations

from pathlib import Path

from gitmem.commands.branch import branch, checkout
from gitmem.commands.commit import commit
from gitmem.commands.context import context
from gitmem.commands.merge import merge
from gitmem.llm import LLMClient
from gitmem.models import BranchMetadata, CommitEntry, ContextResult
from gitmem.workspace import Workspace

__all__ = [
    "GitMem",
    "CommitEntry",
    "BranchMetadata",
    "ContextResult",
    "Workspace",
    "LLMClient",
]


class GitMem:
    """High-level facade wrapping all GitMem operations."""

    def __init__(
        self,
        root: Path | str = ".",
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        self.workspace = Workspace(root)
        self.llm = LLMClient(model)

    def init(self) -> None:
        self.workspace.init()

    async def commit(self, history: str, message: str | None = None) -> CommitEntry:
        return await commit(self.workspace, self.llm, history, message)

    def branch(self, name: str, purpose: str) -> BranchMetadata:
        return branch(self.workspace, name, purpose)

    async def merge(self, source: str, target: str | None = None) -> str:
        return await merge(self.workspace, self.llm, source, target)

    def context(
        self, resolution: str = "medium", query: str | None = None
    ) -> ContextResult:
        return context(self.workspace, resolution, query)

    def checkout(self, name: str) -> None:
        checkout(self.workspace, name)

    def log(self, entry: str) -> None:
        branch_name = self.workspace.read_head()
        self.workspace.append_log(branch_name, entry)
