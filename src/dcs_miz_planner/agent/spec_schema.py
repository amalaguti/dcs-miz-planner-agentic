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
    MissionType.GROUND_ATTACK.value: "manston_ground_attack.yaml",
    MissionType.ESCORT.value: "manston_escort.yaml",
}

# Preferred examples for get_mission_spec_schema / invent (immersion-first).
_AGENT_EXAMPLE_FILES: dict[str, str] = {
    MissionType.FREE_FLIGHT.value: "manston_freeflight_altitude_speed_gates.yaml",
    MissionType.INTERCEPT.value: "manston_dawn_intercept_radio.yaml",
    MissionType.CAP.value: "manston_cap_narrative.yaml",
    MissionType.GROUND_ATTACK.value: "manston_ground_attack_markers.yaml",
    MissionType.ESCORT.value: "manston_escort_narrative.yaml",
}

ANTI_PATTERNS: tuple[str, ...] = (
    'top-level "airfield" / "aircraft" (use nested player.aircraft / player.airfield)',
    '"date" as an ISO string like "1944-06-06" (use {"year","month","day"})',
    'enemies like {"type":"intercept_enemy","id":"..."} (use aircraft + count)',
    "objectives nested under cap or strike (objectives is top-level only)",
    "Lua / script / Mist fields inside triggers (typed when/then only; no free-form script)",
    "friendly / same-coalition targets without strike.practice true",
    "inventing bomb CLSIDs (use named player.payload presets from the catalog)",
)

_TYPE_NOTES: dict[str, tuple[str, ...]] = {
    MissionType.FREE_FLIGHT.value: (
        (
            "enemies, objectives, and targets must be empty lists; omit cap and strike; "
            "omit player.payload."
        ),
        (
            "Immersion OK: non-empty triggers/zones for altitude_speed_gates or "
            "sound_flag_chain (see manston_freeflight_altitude_speed_gates.yaml / "
            "manston_freeflight_sound_flags.yaml)."
        ),
    ),
    MissionType.INTERCEPT.value: (
        'enemies must be non-empty; objectives must include {"type":"intercept_enemy"}.',
        "omit the cap and strike blocks; omit player.payload.",
        (
            "optional narrative.enabled true: expands to typed triggers (scramble / "
            "bandits-down win). Requires empty zones/triggers and enemies; conflicts with "
            "hand-authored triggers."
        ),
        (
            "optional late_activation on enemies; trigger actions radio_item_add / "
            "activate_group for F10 difficulty menus (see manston_dawn_intercept_radio)."
        ),
    ),
    MissionType.CAP.value: (
        "nested cap is required (bearing_deg, distance_km, altitude_m, pattern, engagement).",
        'top-level objectives must include {"type":"patrol"}; enemies are optional.',
        "station is airfield-relative bearing/distance — never invent raw map x/y.",
        "omit strike, targets, and player.payload.",
        (
            "optional narrative.enabled true: expands to typed zones/triggers "
            "(push / on-station / bandits-down win). Requires empty zones/triggers and "
            "at least one enemy; conflicts with hand-authored triggers."
        ),
        "optional late_activation on enemies; radio_item_add / activate_group as for intercept.",
    ),
    MissionType.GROUND_ATTACK.value: (
        "nested strike is required (bearing_deg, distance_km, altitude_m).",
        (
            "player.payload is required (named preset; prefer spitfire_2x250_slipper for "
            "Channel crossings)."
        ),
        (
            "targets must be non-empty. Combat: opposing coalition; land on Axis continent "
            "for Channel WWII; water = ships. Practice (strike.practice true): same-coalition "
            "/ UK-side targets allowed for bombing practice narrative."
        ),
        'objectives must include {"type":"attack_ground"}; enemies must be empty.',
        "omit the cap block. Pilot jettisons the slipper tank in the cockpit before attack.",
        (
            "optional narrative.enabled true: expands to typed zones/triggers (push / "
            "ingress / targets-down win via target_dead). Requires empty zones/triggers, "
            "strike, and targets; conflicts with hand-authored triggers."
        ),
    ),
    MissionType.ESCORT.value: (
        "nested escort is required (bearing_deg, distance_km, altitude_m, engagement).",
        (
            "package must be non-empty and same coalition as the player (friendly only); "
            "e.g. MosquitoFBMkVI."
        ),
        'objectives must include {"type":"escort_package"}; enemies optional (bounce).',
        "destination is airfield-relative bearing/distance — never invent raw map x/y.",
        "omit strike, targets, cap, and player.payload.",
        (
            "optional narrative.enabled true: expands to typed zones/triggers (push / "
            "with-package / bounce-down win). Requires empty zones/triggers, escort, "
            "package, and enemies; conflicts with hand-authored triggers."
        ),
    ),
}

_COMMON_NOTES: tuple[str, ...] = (
    'schema_version must be "1"; theatre for v1 is TheChannel.',
    (
        "Required envelope: schema_version, mission_type, theatre, date, start_time, "
        "weather, player; enemies/objectives/triggers/zones default to empty lists."
    ),
    (
        "Optional typed zones/triggers (no Lua): conditions time_more|flag_is|"
        "flag_equals|flag_more|flag_less|time_since_flag|unit_dead|target_dead|"
        "group_life_less|coalition_in_zone|unit_altitude_higher|unit_altitude_lower|"
        "unit_speed_higher|unit_speed_lower; actions message|set_flag|set_flag_value|"
        "inc_flag|sound|mission_end|radio_item_add|radio_item_remove|activate_group|"
        "deactivate_group|mark|smoke. group_life_less uses enemy_index or target_index "
        "plus percent 1–100 (remaining group life). mark uses zone name + text (F10 "
        "map mark); smoke uses zone name + curated color "
        "(green|red|white|orange|blue). unit_altitude_* use altitude_m and optional "
        "agl (default true, player unit only); unit_speed_* use speed_kmh (player "
        "only). sound uses curated asset_id only "
        "(no paths). enemies/targets may set late_activation true (dormant until "
        "activate_group). Compiler emits native ME trigger tables for validated "
        "graphs. Optional narrative.enabled (cap|intercept|escort|ground_attack) "
        "expands a curated pack into that vocabulary when zones/triggers are empty."
    ),
    "Fill DCS ids and airfield names from tools/prefs — examples are Channel templates.",
    (
        "For creative immersion/challenge: list_mission_options families "
        "mission_inspiration (advisory patterns) and mission_behaviour (supported "
        "recipes with meta.recipe / Spec types / example paths). Optionally "
        "research_guidance(focus=mission_design) and list_installed_campaigns "
        "(Doc filenames by default; include_doc_text for cached PDF excerpts). "
        "Map ideas onto packaged "
        "behaviours only — never Lua or .miz→Spec import. Immersion examples: "
        "manston_freeflight_altitude_speed_gates.yaml, "
        "manston_dawn_intercept_radio.yaml, "
        "manston_cap_narrative.yaml / manston_dawn_intercept_narrative.yaml / "
        "manston_ground_attack_narrative.yaml / manston_escort_narrative.yaml, "
        "manston_freeflight_sound_flags.yaml, "
        "manston_ground_attack_markers.yaml / manston_ground_attack_life_less.yaml."
    ),
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
    """Load and validate the packaged example for ``mission_type`` (immersion-first)."""
    key = (mission_type or "").strip()
    if key not in _EXAMPLE_FILES:
        allowed = ", ".join(supported_mission_types())
        raise ValueError(f"Unsupported mission_type {mission_type!r}; expected one of: {allowed}")
    filename = _AGENT_EXAMPLE_FILES.get(key) or _EXAMPLE_FILES[key]

    path = examples_dir() / filename
    if not path.is_file():
        # Fall back to bare compile example if immersion file missing.
        filename = _EXAMPLE_FILES[key]
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
(free_flight | intercept | cap | ground_attack | escort) and copy that example's structure.
Immersion: after matching the envelope, apply 1–2 mission_behaviour recipes (zones/
triggers, narrative.enabled, late_activation+activate_group, gates, etc.) when the user
left challenge unspecified — see schema notes for example YAML paths.

Always required envelope:
  schema_version, mission_type, theatre, date, start_time, weather, player,
  enemies (list), objectives (list), triggers (list; use [] when unused —
  non-empty OK for supported immersion behaviours), zones (list; [] when unused)

Anti-patterns (fatal):
- top-level airfield/aircraft → use nested player{}
- date as "YYYY-MM-DD" → use {"year","month","day"}
- enemies as {type,id} → use {aircraft,count,...}
- objectives under cap/strike → objectives stay top-level
- friendly ground targets without strike.practice → combat strikes need opposing coalition
- inventing DCS ids / CLSIDs — use tools/prefs and named player.payload only
- late_activation without activate_group (dormant groups — validation rejects)
"""
