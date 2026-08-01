"""Dataclasses for user-memory rows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GenerationRecord:
    id: int
    created_at: str
    prompt: str | None
    mission_type: str | None
    theatre: str | None
    spec_path: str | None
    miz_path: str | None
    outcome: str
    detail: dict[str, Any]


@dataclass(frozen=True)
class FeedbackRecord:
    id: int
    created_at: str
    generation_id: int | None
    score: int | None
    note: str | None
    tags: list[Any]
    source: str
