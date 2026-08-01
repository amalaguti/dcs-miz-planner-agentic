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
    stub_with_research_guidance_then_spec,
)
from .planner import PlanResult, plan_mission
from .prompts import compose_system_prompt
from .realism import channel_date_realism_warnings
from .voice import DEFAULT_VOICE, build_commander_brief, normalize_voice, resolve_voice

__all__ = [
    "DEFAULT_VOICE",
    "ENV_API_KEY",
    "ENV_BASE_URL",
    "ENV_MODEL",
    "AgentConfigError",
    "OpenAILLM",
    "PlanResult",
    "StubLLM",
    "build_commander_brief",
    "channel_date_realism_warnings",
    "compose_system_prompt",
    "live_llm_from_env",
    "normalize_voice",
    "plan_mission",
    "resolve_voice",
    "stub_with_find_airfield_then_spec",
    "stub_with_get_user_prefs_then_spec",
    "stub_with_research_guidance_then_spec",
]
