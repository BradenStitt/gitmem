---
doc_type: feature_design
feature_id: F-001
status: design_draft
last_updated: 2026-03-05
---
# Workspace File System Design

## Architecture

The Workspace layer is a pure-filesystem abstraction with no LLM dependencies. It provides all I/O operations for the `.gitmem/` directory structure.

```
src/gitmem/
├── workspace.py    # Workspace class — all file I/O
├── models.py       # Pydantic data models (CommitEntry, BranchMetadata, ContextResult)
└── templates.py    # Default content for initialized files
```

On-disk layout managed by `Workspace`:

```
.gitmem/
├── main.md                         # Global project roadmap
├── HEAD                            # Current branch name (plain text)
└── branches/
    └── <branch-name>/
        ├── commit.md               # Append-only structured commit log
        ├── log.md                   # Detailed OTA execution traces
        └── metadata.yaml           # Branch metadata (YAML)
```

## Interfaces / Contracts

```python
class Workspace:
    def __init__(self, root: Path = Path.cwd()) -> None
    def init(self) -> None                                          # R-F001-001, R-F001-002
    def read_head(self) -> str                                      # R-F001-005
    def write_head(self, branch: str) -> None                       # R-F001-005
    def read_main(self) -> str                                      # R-F001-007
    def write_main(self, content: str) -> None                      # R-F001-007
    def read_commits(self, branch: str) -> list[CommitEntry]        # R-F001-009
    def append_commit(self, branch: str, entry: CommitEntry) -> None # R-F001-009
    def read_log(self, branch: str) -> str                          # R-F001-010
    def append_log(self, branch: str, entry: str) -> None           # R-F001-010
    def read_metadata(self, branch: str) -> BranchMetadata          # R-F001-008
    def write_metadata(self, branch: str, meta: BranchMetadata) -> None # R-F001-008
    def create_branch_dir(self, name: str) -> None                  # R-F001-006
    def list_branches(self) -> list[str]                            # R-F001-006
    def branch_exists(self, name: str) -> bool                      # R-F001-006
```

## Data Model

```python
class CommitEntry(BaseModel):
    id: str                    # e.g., "C-001"
    timestamp: datetime
    branch: str
    summary: str
    progress: str
    current_state: str
    next_steps: list[str]

class BranchMetadata(BaseModel):
    name: str
    parent: str | None
    purpose: str
    created_at: datetime
    status: Literal["active", "merged", "abandoned"]

class ContextResult(BaseModel):
    resolution: Literal["low", "medium", "high"]
    content: str
    source: str
```

## Error Handling

- `WorkspaceExistsError` raised when `init()` is called on existing workspace (R-F001-003).
- `BranchNotFoundError` raised when accessing a non-existent branch directory.
- `WorkspaceNotInitializedError` raised when operating on an uninitialized workspace.

## Security / Privacy

- No secrets stored in `.gitmem/` files.
- Workspace is scoped to a single directory tree — no path traversal outside `root`.

## Testing Strategy

- Unit tests using `tmp_path` fixture for isolated filesystem operations.
- Test init, read/write for each file type, error cases.

## Requirement Mapping

- D-F001-001: `Workspace.init()` creates the full directory structure. Implements R-F001-001, R-F001-002.
- D-F001-002: `Workspace.read_head()` / `write_head()` manage the HEAD file. Implements R-F001-005.
- D-F001-003: `Workspace.list_branches()` / `branch_exists()` / `create_branch_dir()` manage branch directories. Implements R-F001-006.
- D-F001-004: `Workspace.read_main()` / `write_main()` manage the roadmap file. Implements R-F001-007.
- D-F001-005: `Workspace.read_metadata()` / `write_metadata()` manage branch metadata YAML. Implements R-F001-008.
- D-F001-006: `Workspace.read_commits()` / `append_commit()` manage commit logs. Implements R-F001-009.
- D-F001-007: `Workspace.read_log()` / `append_log()` manage execution trace logs. Implements R-F001-010.
- D-F001-008: All file I/O goes through the `Workspace` class. Implements R-F001-004.
