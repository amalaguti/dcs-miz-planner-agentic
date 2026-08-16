"""LLM client protocol, stub, and OpenAI-compatible live adapter."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Protocol

from .tool_bridge import TOOL_DEFINITIONS

DEFAULT_MODEL = "gpt-4o-mini"
ENV_API_KEY = "OPENAI_API_KEY"
ENV_MODEL = "DCS_MIZ_LLM_MODEL"
ENV_BASE_URL = "OPENAI_BASE_URL"

# Canned Manston free-flight Spec JSON for stub / offline demos.
MANSTON_FREE_FLIGHT_JSON = json.dumps(
    {
        "schema_version": "1",
        "mission_type": "free_flight",
        "theatre": "TheChannel",
        "name": "Manston Free Flight",
        "description": "Cold start at Manston. Free flight over the Channel. Clear morning.",
        "date": {"year": 1944, "month": 6, "day": 6},
        "start_time": "09:00",
        "weather": "sunny_clear",
        "player": {
            "aircraft": "SpitfireLFMkIX",
            "airfield": "Manston",
            "coalition": "blue",
            "country": "UK",
            "skill": "Player",
            "start": "cold_parking",
        },
        "enemies": [],
        "objectives": [],
        "triggers": [],
    }
)

# Optional test-only Batumi free-flight JSON (stub default stays Manston).
BATUMI_COLD_FREE_FLIGHT_JSON = json.dumps(
    {
        "schema_version": "1",
        "mission_type": "free_flight",
        "theatre": "Caucasus",
        "name": "Batumi Free Flight",
        "description": "Cold start at Batumi. Free flight over the Caucasus. Clear morning.",
        "date": {"year": 2024, "month": 6, "day": 6},
        "start_time": "09:00",
        "weather": "sunny_clear",
        "player": {
            "aircraft": "Su-25T",
            "airfield": "Batumi",
            "coalition": "blue",
            "country": "Georgia",
            "skill": "Player",
            "start": "cold_parking",
        },
        "enemies": [],
        "objectives": [],
        "triggers": [],
    }
)

# Optional test-only Needs Oar Point free-flight JSON (stub default stays Manston).
NEEDS_OAR_POINT_FREE_FLIGHT_JSON = json.dumps(
    {
        "schema_version": "1",
        "mission_type": "free_flight",
        "theatre": "Normandy",
        "name": "Needs Oar Point Free Flight",
        "description": "Cold start at Needs Oar Point. Free flight over Normandy. Clear morning.",
        "date": {"year": 1944, "month": 6, "day": 6},
        "start_time": "09:00",
        "weather": "sunny_clear",
        "player": {
            "aircraft": "SpitfireLFMkIX",
            "airfield": "NeedsOarPoint",
            "coalition": "blue",
            "country": "UK",
            "skill": "Player",
            "start": "cold_parking",
        },
        "enemies": [],
        "objectives": [],
        "triggers": [],
    }
)


class AgentConfigError(ValueError):
    """Missing or invalid live LLM configuration."""


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: str


@dataclass(frozen=True)
class LLMResponse:
    content: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()


class LLMClient(Protocol):
    def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse: ...


@dataclass
class StubLLM:
    """Offline LLM: optional scripted turns, else return Manston free-flight JSON."""

    script: list[LLMResponse] = field(default_factory=list)
    _index: int = 0

    def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        del messages, tools
        if self._index < len(self.script):
            resp = self.script[self._index]
            self._index += 1
            return resp
        return LLMResponse(content=MANSTON_FREE_FLIGHT_JSON)


def stub_with_find_airfield_then_spec() -> StubLLM:
    """Script: call find_airfield, then emit Manston Spec JSON."""
    return StubLLM(
        script=[
            LLMResponse(
                tool_calls=(
                    ToolCall(
                        id="call_1",
                        name="find_airfield",
                        arguments=json.dumps({"query": "Manston"}),
                    ),
                )
            ),
            LLMResponse(content=MANSTON_FREE_FLIGHT_JSON),
        ]
    )


def stub_with_get_user_prefs_then_spec() -> StubLLM:
    """Script: call get_user_prefs, then emit Manston Spec JSON."""
    return StubLLM(
        script=[
            LLMResponse(
                tool_calls=(
                    ToolCall(
                        id="call_prefs",
                        name="get_user_prefs",
                        arguments="{}",
                    ),
                )
            ),
            LLMResponse(content=MANSTON_FREE_FLIGHT_JSON),
        ]
    )


def stub_with_research_guidance_then_spec() -> StubLLM:
    """Script: call research_guidance, then emit Manston Spec JSON."""
    return StubLLM(
        script=[
            LLMResponse(
                tool_calls=(
                    ToolCall(
                        id="call_research",
                        name="research_guidance",
                        arguments=json.dumps(
                            {
                                "query": "Spitfire Channel free flight procedures",
                                "mission_type": "free_flight",
                                "theatre": "TheChannel",
                                "aircraft": "SpitfireLFMkIX",
                            }
                        ),
                    ),
                )
            ),
            LLMResponse(content=MANSTON_FREE_FLIGHT_JSON),
        ]
    )


def stub_chat_clarify_then_spec() -> StubLLM:
    """Multi-turn chat stub: clarify, optional tool, then Spec JSON."""
    return StubLLM(
        script=[
            LLMResponse(
                content=(
                    "Right. Free flight or CAP from Manston? "
                    "Say the word and I'll draft the Spec for /accept."
                )
            ),
            LLMResponse(
                tool_calls=(
                    ToolCall(
                        id="call_af",
                        name="find_airfield",
                        arguments=json.dumps({"query": "Manston"}),
                    ),
                )
            ),
            LLMResponse(content=MANSTON_FREE_FLIGHT_JSON),
        ]
    )


@dataclass
class OpenAILLM:
    """Live OpenAI-compatible chat client."""

    api_key: str
    model: str = DEFAULT_MODEL
    base_url: str | None = None

    def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        from openai import OpenAI

        kwargs: dict[str, Any] = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        client = OpenAI(**kwargs)
        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            create_kwargs["tools"] = tools
        completion = client.chat.completions.create(**create_kwargs)
        msg = completion.choices[0].message
        tool_calls: list[ToolCall] = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=tc.function.arguments or "{}",
                    )
                )
        return LLMResponse(
            content=msg.content,
            tool_calls=tuple(tool_calls),
        )


def live_llm_from_env(*, env: dict[str, str] | None = None) -> OpenAILLM:
    """Build a live client from environment; raise if API key missing."""
    if env is None:
        from ..env_load import load_local_dotenv

        load_local_dotenv()
    env = env if env is not None else dict(os.environ)
    key = (env.get(ENV_API_KEY) or "").strip()
    if not key:
        raise AgentConfigError(
            f"Live planning requires {ENV_API_KEY}. "
            f"Set that environment variable, put it in a local .env file "
            f"(see .env.example), or pass --stub for offline mode."
        )
    model = (env.get(ENV_MODEL) or DEFAULT_MODEL).strip() or DEFAULT_MODEL
    base = (env.get(ENV_BASE_URL) or "").strip() or None
    return OpenAILLM(api_key=key, model=model, base_url=base)


def default_tools() -> list[dict[str, Any]]:
    return list(TOOL_DEFINITIONS)
