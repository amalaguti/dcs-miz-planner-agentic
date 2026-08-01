"""User memory: prefs, generation history, and satisfaction feedback."""

from __future__ import annotations

from ..install.store import default_db_path
from .models import FeedbackRecord, GenerationRecord
from .service import (
    OUTCOME_COMPILE_FAILED,
    OUTCOME_FAILED,
    OUTCOME_SUCCESS,
    OUTCOME_VALIDATION_FAILED,
    SEED_PREF_KEYS,
    UserMemoryService,
)
from .store import USER_SCHEMA_VERSION, UserMemoryStore

__all__ = [
    "OUTCOME_COMPILE_FAILED",
    "OUTCOME_FAILED",
    "OUTCOME_SUCCESS",
    "OUTCOME_VALIDATION_FAILED",
    "SEED_PREF_KEYS",
    "USER_SCHEMA_VERSION",
    "FeedbackRecord",
    "GenerationRecord",
    "UserMemoryService",
    "UserMemoryStore",
    "default_db_path",
]
