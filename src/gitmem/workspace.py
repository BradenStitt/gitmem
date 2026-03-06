"""Workspace — filesystem layer for .gitmem/ directory management."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import yaml

from gitmem.errors import (
    BranchNotFoundError,
    WorkspaceExistsError,
    WorkspaceNotInitializedError,
)
from gitmem.models import BranchMetadata, CommitEntry
from gitmem.templates import (
    COMMIT_MD_DEFAULT,
    HEAD_DEFAULT,
    LOG_MD_DEFAULT,
    MAIN_MD_DEFAULT,
)

_COMMIT_SEPARATOR = "\n---\n"


class Workspace:
    """Manages all file I/O for the .gitmem/ workspace directory."""

    def __init__(self, root: Path | str = ".") -> None:
        self.root = Path(root).resolve()
        self.gitmem_dir = self.root / ".gitmem"

    def _ensure_initialized(self) -> None:
        if not self.gitmem_dir.is_dir():
            raise WorkspaceNotInitializedError(
                f"No .gitmem/ directory found at {self.root}"
            )

    def _branch_dir(self, branch: str) -> Path:
        d = self.gitmem_dir / "branches" / branch
        if not d.is_dir():
            raise BranchNotFoundError(f"Branch '{branch}' does not exist")
        return d

    # --- Init ---

    def init(self) -> None:
        """Create the full .gitmem/ workspace structure with a main branch."""
        if self.gitmem_dir.exists():
            raise WorkspaceExistsError(
                f"Workspace already initialized at {self.gitmem_dir}"
            )

        # Create directory structure
        main_branch_dir = self.gitmem_dir / "branches" / "main"
        main_branch_dir.mkdir(parents=True)

        # Write root files
        (self.gitmem_dir / "HEAD").write_text(HEAD_DEFAULT)
        (self.gitmem_dir / "main.md").write_text(MAIN_MD_DEFAULT)

        # Write branch files
        (main_branch_dir / "commit.md").write_text(COMMIT_MD_DEFAULT)
        (main_branch_dir / "log.md").write_text(LOG_MD_DEFAULT)

        now = datetime.now(UTC)
        meta = BranchMetadata(
            name="main",
            parent=None,
            purpose="Main development branch",
            created_at=now,
            status="active",
        )
        self.write_metadata("main", meta, _skip_check=True)

    # --- HEAD ---

    def read_head(self) -> str:
        self._ensure_initialized()
        return (self.gitmem_dir / "HEAD").read_text().strip()

    def write_head(self, branch: str) -> None:
        self._ensure_initialized()
        (self.gitmem_dir / "HEAD").write_text(branch)

    # --- main.md ---

    def read_main(self) -> str:
        self._ensure_initialized()
        return (self.gitmem_dir / "main.md").read_text()

    def write_main(self, content: str) -> None:
        self._ensure_initialized()
        (self.gitmem_dir / "main.md").write_text(content)

    # --- Branches ---

    def list_branches(self) -> list[str]:
        self._ensure_initialized()
        branches_dir = self.gitmem_dir / "branches"
        return sorted(d.name for d in branches_dir.iterdir() if d.is_dir())

    def branch_exists(self, name: str) -> bool:
        self._ensure_initialized()
        return (self.gitmem_dir / "branches" / name).is_dir()

    def create_branch_dir(self, name: str) -> None:
        self._ensure_initialized()
        branch_dir = self.gitmem_dir / "branches" / name
        branch_dir.mkdir(parents=True)
        (branch_dir / "commit.md").write_text(COMMIT_MD_DEFAULT)
        (branch_dir / "log.md").write_text(LOG_MD_DEFAULT)

    # --- Metadata ---

    def read_metadata(self, branch: str) -> BranchMetadata:
        d = self._branch_dir(branch)
        raw = yaml.safe_load((d / "metadata.yaml").read_text())
        return BranchMetadata(**raw)

    def write_metadata(
        self, branch: str, meta: BranchMetadata, *, _skip_check: bool = False
    ) -> None:
        if not _skip_check:
            d = self._branch_dir(branch)
        else:
            d = self.gitmem_dir / "branches" / branch
        data = meta.model_dump()
        data["created_at"] = data["created_at"].isoformat()
        (d / "metadata.yaml").write_text(yaml.dump(data, default_flow_style=False))

    # --- Commits ---

    def read_commits(self, branch: str) -> list[CommitEntry]:
        d = self._branch_dir(branch)
        content = (d / "commit.md").read_text().strip()
        if not content:
            return []

        entries = []
        for block in content.split(_COMMIT_SEPARATOR):
            block = block.strip()
            if not block:
                continue
            data = json.loads(block)
            entries.append(CommitEntry(**data))
        return entries

    def append_commit(self, branch: str, entry: CommitEntry) -> None:
        d = self._branch_dir(branch)
        commit_file = d / "commit.md"
        existing = commit_file.read_text().strip()
        serialized = entry.model_dump_json(indent=2)
        if existing:
            commit_file.write_text(existing + _COMMIT_SEPARATOR + serialized + "\n")
        else:
            commit_file.write_text(serialized + "\n")

    # --- Log ---

    def read_log(self, branch: str) -> str:
        d = self._branch_dir(branch)
        return (d / "log.md").read_text()

    def append_log(self, branch: str, entry: str) -> None:
        d = self._branch_dir(branch)
        log_file = d / "log.md"
        existing = log_file.read_text()
        log_file.write_text(existing + entry + "\n")
