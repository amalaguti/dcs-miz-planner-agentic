"""Natural-language → Mission Spec agent."""

from __future__ import annotations

from .llm import (
    ENV_API_KEY,
    ENV_BASE_URL,
    ENV_MODEL,
    AgentConfigError,
    OpenAILLM,
    StubLLM,
    live_llm_from_env,
    stub_with_find_airfield_then_spec,
    stub_with_get_user_prefs_then_spec,
)
from .planner import PlanResult, plan_mission
from .realism import channel_date_realism_warnings

__all__ = [
    "ENV_API_KEY",
    "ENV_BASE_URL",
    "ENV_MODEL",
    "AgentConfigError",
    "OpenAILLM",
    "PlanResult",
    "StubLLM",
    "channel_date_realism_warnings",
    "live_llm_from_env",
    "plan_mission",
    "stub_with_find_airfield_then_spec",
    "stub_with_get_user_prefs_then_spec",
]
