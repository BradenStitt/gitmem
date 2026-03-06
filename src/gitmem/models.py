"""Pydantic data models for GitMem."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class CommitEntry(BaseModel):
    id: str
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
