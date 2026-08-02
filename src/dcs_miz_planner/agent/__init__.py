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
    stub_chat_clarify_then_spec,
    stub_with_find_airfield_then_spec,
    stub_with_get_user_prefs_then_spec,
    stub_with_research_guidance_then_spec,
)
from .planner import PlanResult, plan_mission
from .prompts import compose_system_prompt
from .realism import channel_date_realism_warnings
from .session import PlanSession, run_chat_repl
from .verbose import DEFAULT_VERBOSE
from .voice import DEFAULT_VOICE, build_commander_brief, normalize_voice, resolve_voice

__all__ = [
    "DEFAULT_VERBOSE",
    "DEFAULT_VOICE",
    "ENV_API_KEY",
    "ENV_BASE_URL",
    "ENV_MODEL",
    "AgentConfigError",
    "OpenAILLM",
    "PlanResult",
    "PlanSession",
    "StubLLM",
    "build_commander_brief",
    "channel_date_realism_warnings",
    "compose_system_prompt",
    "live_llm_from_env",
    "normalize_voice",
    "plan_mission",
    "resolve_voice",
    "run_chat_repl",
    "stub_chat_clarify_then_spec",
    "stub_with_find_airfield_then_spec",
    "stub_with_get_user_prefs_then_spec",
    "stub_with_research_guidance_then_spec",
]
