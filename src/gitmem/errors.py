"""GitMem error types."""


class GitMemError(Exception):
    """Base error for all GitMem operations."""


class WorkspaceExistsError(GitMemError):
    """Raised when init() is called on an existing workspace."""


class WorkspaceNotInitializedError(GitMemError):
    """Raised when operating on an uninitialized workspace."""


class BranchExistsError(GitMemError):
    """Raised when creating a branch that already exists."""


class BranchNotFoundError(GitMemError):
    """Raised when accessing a non-existent branch."""
