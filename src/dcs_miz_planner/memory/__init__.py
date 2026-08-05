"""User memory: prefs, generation history, and satisfaction feedback."""

from __future__ import annotations

from ..install.store import default_db_path
from .creative import (
    CREATIVITY_ASSERTIVE,
    CREATIVITY_MAX,
    CREATIVITY_QUIET,
    PREF_AVOID_BEHAVIOURS,
    PREF_CREATIVITY_LEVEL,
    PREF_PREFERRED_BEHAVIOURS,
    CreativeBias,
    build_creative_detail,
    creative_bias_from_history,
    detail_with_inferred_creative,
    format_creative_bias_fragment,
    infer_creative_from_spec,
    load_creative_bias,
    merge_creative_into_detail,
)
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
    "CREATIVITY_ASSERTIVE",
    "CREATIVITY_MAX",
    "CREATIVITY_QUIET",
    "OUTCOME_COMPILE_FAILED",
    "OUTCOME_FAILED",
    "OUTCOME_SUCCESS",
    "OUTCOME_VALIDATION_FAILED",
    "PREF_AVOID_BEHAVIOURS",
    "PREF_CREATIVITY_LEVEL",
    "PREF_PREFERRED_BEHAVIOURS",
    "SEED_PREF_KEYS",
    "USER_SCHEMA_VERSION",
    "CreativeBias",
    "FeedbackRecord",
    "GenerationRecord",
    "UserMemoryService",
    "UserMemoryStore",
    "build_creative_detail",
    "creative_bias_from_history",
    "default_db_path",
    "detail_with_inferred_creative",
    "format_creative_bias_fragment",
    "infer_creative_from_spec",
    "load_creative_bias",
    "merge_creative_into_detail",
]
