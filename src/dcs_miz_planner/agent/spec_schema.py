"""Derived Mission Spec examples for agent prompts and tools.

Source of truth remains ``MissionSpec`` + checked-in ``examples/*.yaml``.
This module projects compact, LLM-friendly examples — not a second schema SoT.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..loader import load_mission_spec
from ..models import MissionSpec, MissionType

_EXAMPLE_FILES: dict[str, str] = {
    MissionType.FREE_FLIGHT.value: "manston_cold_freeflight.yaml",
    MissionType.INTERCEPT.value: "manston_dawn_intercept.yaml",
    MissionType.CAP.value: "manston_cap.yaml",
}

ANTI_PATTERNS: tuple[str, ...] = (
    'top-level "airfield" / "aircraft" (use nested player.aircraft / player.airfield)',
    '"date" as an ISO string like "1944-06-06" (use {"year","month","day"})',
    'enemies like {"type":"intercept_enemy","id":"..."} (use aircraft + count)',
    "objectives nested under cap (objectives is top-level only)",
    "omitting theatre, player, or triggers (triggers must be [])",
)

_TYPE_NOTES: dict[str, tuple[str, ...]] = {
    MissionType.FREE_FLIGHT.value: (
        "enemies and objectives must be empty lists; omit the cap block.",
    ),
    MissionType.INTERCEPT.value: (
        'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
        "omit the cap block.",
    ),
    MissionType.CAP.value: (
        "nested cap is required (bearing_deg, distance_km, altitude_m, pattern, engagement).",
        'top-level objectives must include {"type":"patrol"}; enemies are optional.',
        "station is airfield-relative bearing/distance — never invent raw map x/y.",
    ),
}

_COMMON_NOTES: tuple[str, ...] = (
    'schema_version must be "1"; theatre for v1 is TheChannel.',
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player, enemies, objectives, triggers."
    ),
    "Fill DCS ids and airfield names from tools/prefs — examples are Channel templates.",
    "Call get_mission_spec_schema for the mission_type before emitting Spec JSON.",
)

_MT_IN_JSON = re.compile(r'"mission_type"\s*:\s*"([a-z_]+)"')


@dataclass(frozen=True)
class SpecSchemaView:
    mission_type: str
    example: dict[str, Any]
    notes: tuple[str, ...]
    anti_patterns: tuple[str, ...] = ANTI_PATTERNS


def examples_dir() -> Path:
    """Repo ``examples/`` directory (…/src/dcs_miz_planner/agent → parents[3])."""
    return Path(__file__).resolve().parents[3] / "examples"


def supported_mission_types() -> tuple[str, ...]:
    return tuple(_EXAMPLE_FILES.keys())


def build_spec_schema(mission_type: str) -> SpecSchemaView:
    """Load and validate the packaged example for ``mission_type``."""
    key = (mission_type or "").strip()
    filename = _EXAMPLE_FILES.get(key)
    if filename is None:
        allowed = ", ".join(supported_mission_types())
        raise ValueError(f"Unsupported mission_type {mission_type!r}; expected one of: {allowed}")

    path = examples_dir() / filename
    if not path.is_file():
        raise FileNotFoundError(f"Missing Spec example for {key}: {path}")

    spec = load_mission_spec(path)
    if spec.mission_type.value != key:
        raise ValueError(
            f"Example {path.name} has mission_type {spec.mission_type.value!r}, expected {key!r}"
        )
    example = json.loads(spec.model_dump_json())
    # Re-validate the projected dict so drift fails loudly.
    MissionSpec.model_validate(example)
    notes = _COMMON_NOTES + _TYPE_NOTES.get(key, ())
    return SpecSchemaView(mission_type=key, example=example, notes=notes)


def infer_mission_type(text: str | None, *, default: str = MissionType.FREE_FLIGHT.value) -> str:
    """Best-effort ``mission_type`` from rejected Spec text; else ``default``."""
    if not text:
        return default
    m = _MT_IN_JSON.search(text)
    if m and m.group(1) in _EXAMPLE_FILES:
        return m.group(1)
    return default


def format_spec_schema_fragment(view: SpecSchemaView) -> str:
    """Human/LLM-readable example + notes for prompts and repair nudges."""
    example_json = json.dumps(view.example, indent=2, ensure_ascii=False)
    notes = "\n".join(f"- {n}" for n in view.notes)
    antis = "\n".join(f"- {a}" for a in view.anti_patterns)
    return (
        f"Mission Spec example for mission_type={view.mission_type!r} "
        f"(derived from packaged examples; validate before accept):\n"
        f"{example_json}\n\n"
        f"Notes:\n{notes}\n\n"
        f"DO NOT emit:\n{antis}"
    )


# Thin always-on reminder for the system prompt (no full skeletons).
SPEC_SHAPE_REMINDER = """\
Mission Spec JSON (schema_version "1") — extra fields are rejected.
Before emitting Spec JSON, call get_mission_spec_schema with the mission_type
(free_flight | intercept | cap) and copy that example's structure.

Always required envelope:
  schema_version, mission_type, theatre, date, start_time, weather, player,
  enemies (list), objectives (list), triggers (must be [])

Anti-patterns (fatal):
- top-level airfield/aircraft → use nested player{}
- date as "YYYY-MM-DD" → use {"year","month","day"}
- enemies as {type,id} → use {aircraft,count,...}
- objectives under cap → objectives stay top-level
- inventing DCS ids — use tools/prefs only
"""
