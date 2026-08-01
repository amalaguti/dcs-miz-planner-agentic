"""Service façade over UserMemoryStore."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..install.store import default_db_path
from .models import FeedbackRecord, GenerationRecord
from .store import UserMemoryStore

OUTCOME_SUCCESS = "success"
OUTCOME_VALIDATION_FAILED = "validation_failed"
OUTCOME_COMPILE_FAILED = "compile_failed"
OUTCOME_FAILED = "failed"

SEED_PREF_KEYS = (
    "preferred_aircraft",
    "preferred_airfield",
    "preferred_start_type",
    "preferred_weather",
    "squadron_voice",
)


class UserMemoryService:
    """User prefs / history / feedback on the shared inventory SQLite path."""

    def __init__(self, db_path: Path | str | None = None) -> None:
        self.db_path = Path(db_path) if db_path is not None else default_db_path()
        self.store = UserMemoryStore(self.db_path)

    def get_prefs(self, keys: list[str] | None = None) -> dict[str, Any]:
        return self.store.get_prefs(keys)

    def set_prefs(self, prefs: dict[str, Any]) -> dict[str, Any]:
        return self.store.set_prefs(prefs)

    def record_generation(
        self,
        *,
        outcome: str,
        prompt: str | None = None,
        mission_type: str | None = None,
        theatre: str | None = None,
        spec_path: str | None = None,
        miz_path: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> int:
        return self.store.append_generation(
            outcome=outcome,
            prompt=prompt,
            mission_type=mission_type,
            theatre=theatre,
            spec_path=spec_path,
            miz_path=miz_path,
            detail=detail,
        )

    def list_generations(self, *, limit: int = 20) -> list[GenerationRecord]:
        return self.store.list_generations(limit=limit)

    def record_feedback(
        self,
        *,
        source: str,
        generation_id: int | None = None,
        score: int | None = None,
        note: str | None = None,
        tags: list[Any] | None = None,
    ) -> int:
        return self.store.add_feedback(
            source=source,
            generation_id=generation_id,
            score=score,
            note=note,
            tags=tags,
        )

    def list_feedback(self, *, limit: int = 20) -> list[FeedbackRecord]:
        return self.store.list_feedback(limit=limit)
