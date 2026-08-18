"""Bridge OpenAI-style tool definitions to dcs_miz_planner.tools."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..tools import (
    compile_mission,
    find_airfield,
    get_aircraft_details,
    get_mission_spec_schema,
    get_user_prefs,
    list_generation_history,
    list_installed_campaigns,
    list_mission_options,
    list_strike_targets,
    randomize_mission,
    record_feedback,
    record_generation,
    research_guidance,
    reweather_mission_file,
    set_user_prefs,
    validate_mission_spec,
)

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "find_airfield",
            "description": "Find known catalog airfields by name substring.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Airfield name query"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_aircraft_details",
            "description": "Get known aircraft id and radio frequency from the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "aircraft_id": {"type": "string"},
                },
                "required": ["aircraft_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_mission_options",
            "description": (
                "List known mission enums, offerable theatres, and enriched planning "
                "options with support levels (supported|advisory|future). Includes "
                "mission_behaviour / mission_inspiration (immersion recipes), plus "
                "mission-designer shelves dynamics_mode (Spec dynamics.mode), "
                "strike_target_class, ground_ai_preset, and channel_place. channel_place "
                "meta includes strike_bearing_deg/strike_distance_km (and aoi_*) recipes "
                "plus french_coast path_point_deltas for short land paths — copy those "
                "for GA/recon geometry. Harbour/dock → coastal_harbour + sea units only. "
                "Pass theatre so Channel invent does not copy Normandy places (and vice "
                "versa). For targets[] invent: call this first (preferred_motion / "
                "preferred_ai_preset / cues / geometry), then list_strike_targets "
                "(domain=sea for harbour), then emit allowlisted unit + motion + "
                "ai_preset only — no free-form ME Opt*."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "theatre": {
                        "type": "string",
                        "description": (
                            "Optional theatre id; filters channel_place by meta.theatre"
                        ),
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_strike_targets",
            "description": (
                "List known Channel strike/recon unit targets from the catalog "
                "(land + sea). Call after list_mission_options and before inventing "
                "ground_attack or recon targets[]. Optional filters: domain "
                "(land|sea), class_id (soft_vehicles, aaa_guns, sea_craft, …), "
                "q (substring on unit_id/label), theatre (TheChannel combat; "
                "Normandy returns WWII land units; sea_craft stay Channel-only). Harbour/dock "
                "asks MUST use domain=sea. Prefer returned exact DCS unit_ids; pair "
                "with shelf preferred_motion / preferred_ai_preset (convoy_transit, "
                "aaa_alert, ship_under_way, harbour_static)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Optional land | sea",
                    },
                    "class_id": {
                        "type": "string",
                        "description": "Optional strike_target_class id",
                    },
                    "q": {
                        "type": "string",
                        "description": "Optional substring match on unit_id or label",
                    },
                    "theatre": {
                        "type": "string",
                        "description": "Optional theatre id (TheChannel combat; Normandy empty)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_installed_campaigns",
            "description": (
                "List local DCS campaigns under Mods/campaigns (names, .miz files, "
                "Doc/ PDFs, short .cmp description). Inspiration only — never import "
                ".miz as Spec. Default: Doc filenames only. Set include_doc_text=true "
                "for short PDF excerpts (cached by file mtime/size; unchanged Docs are "
                "not re-parsed). Prefer Doc themes when excerpts exist; else filenames."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "include_doc_text": {
                        "type": "boolean",
                        "description": (
                            "If true, return short Doc PDF excerpts (cached). "
                            "Default false = filenames only."
                        ),
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_mission_spec_schema",
            "description": (
                "Get a compact Mission Spec JSON example plus notes/anti-patterns for a "
                "mission_type (free_flight, intercept, cap, ground_attack, escort, or recon). "
                "Optional theatre: TheChannel uses Manston examples; Normandy all six "
                "types use NeedsOarPoint; Caucasus all six types "
                "use Batumi; Syria all six types "
                "use Incirlik; Nevada all six types "
                "use Nellis (CAP/intercept/escort 350° / 40 km desert north-range; "
                "GA/recon 303° / 85 km inland past Creech); Falklands "
                "free_flight, CAP, intercept, or escort uses Mount Pleasant (150° / 40 km South Atlantic). "
                "Falklands ground_attack / recon "
                "are unsupported. Call before "
                "emitting Spec JSON."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "mission_type": {
                        "type": "string",
                        "description": "free_flight | intercept | cap | ground_attack | escort | recon",
                    },
                    "theatre": {
                        "type": "string",
                        "description": "Optional theatre id (TheChannel, Normandy, Caucasus, Syria, Nevada, Falklands)",
                    },
                },
                "required": ["mission_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_prefs",
            "description": (
                "Read stored user preferences (preferred airfield, aircraft, weather, "
                "start type, squadron_voice, etc.). Call early; honor prefs when the "
                "user left a knob unspecified."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keys": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional preference keys to fetch",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_user_prefs",
            "description": "Upsert one or more user preference keys (JSON values).",
            "parameters": {
                "type": "object",
                "properties": {
                    "prefs": {
                        "type": "object",
                        "description": "Map of preference key → value",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_generation_history",
            "description": (
                "List recent mission generations (newest first). When inventing "
                "immersion, prefer detail.creative behaviours that scored well; "
                "soft-avoid poorly scored ones."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Max rows (default 20)"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_generation",
            "description": (
                "Record a generation outcome. The host also auto-records; use when "
                "explicitly logging an attempt. Optional detail.creative may include "
                "inspirations, behaviours (mission_behaviour ids), and sources "
                "(catalog|campaign_doc|research|user_request)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "outcome": {
                        "type": "string",
                        "description": "success | validation_failed | compile_failed | failed",
                    },
                    "prompt": {"type": "string"},
                    "mission_type": {"type": "string"},
                    "theatre": {"type": "string"},
                    "spec_path": {"type": "string"},
                    "miz_path": {"type": "string"},
                    "detail": {
                        "type": "object",
                        "description": (
                            "Optional metadata; include creative={inspirations,behaviours,sources} "
                            "when immersion recipes were applied"
                        ),
                    },
                },
                "required": ["outcome"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_feedback",
            "description": (
                "Record satisfaction feedback (score/note/tags). Tags may name "
                "behaviours as liked:altitude_speed_gates or avoid:narrative_pack."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "score": {"type": "integer"},
                    "note": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "generation_id": {"type": "integer"},
                    "source": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "research_guidance",
            "description": (
                "Research short notes on flight procedures, combat manoeuvres, "
                "pilot accounts, historical context, or (with focus=mission_design) "
                "how others built DCS missions (User Files / repos / ME patterns). "
                "Map ideas onto mission_behaviour cards. Not a source of DCS type ids "
                "or Spec fields."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to research"},
                    "mission_type": {
                        "type": "string",
                        "description": "Optional: free_flight, intercept, …",
                    },
                    "theatre": {"type": "string"},
                    "aircraft": {"type": "string"},
                    "focus": {
                        "type": "string",
                        "description": (
                            "Optional: tactics (default) or mission_design for "
                            "User Files / mission-repo / ME pattern bias"
                        ),
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "validate_mission_spec",
            "description": "Validate a Mission Spec YAML file path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spec_path": {"type": "string"},
                },
                "required": ["spec_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compile_mission",
            "description": (
                "Compile a Mission Spec YAML to a .miz file. "
                "Optional voice (raf|usaaf|neutral) selects briefing l10n register."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spec_path": {"type": "string"},
                    "output_path": {"type": "string"},
                    "voice": {
                        "type": "string",
                        "description": "Optional: raf | usaaf | neutral for .miz briefing text",
                    },
                },
                "required": ["spec_path", "output_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reweather_mission",
            "description": (
                "Change weather on an existing .miz and overwrite it. Prefers sibling "
                "Spec YAML recompile; otherwise patches the weather table. Optional seed; "
                "omitted seed draws a new invent day."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "miz_path": {"type": "string"},
                    "weather": {
                        "type": "string",
                        "description": "WeatherPreset id (e.g. rain_overcast, broken_channel)",
                    },
                    "seed": {"type": "integer", "description": "Optional invent seed"},
                    "spec_path": {
                        "type": "string",
                        "description": "Optional Spec YAML path (else sibling of .miz)",
                    },
                    "voice": {
                        "type": "string",
                        "description": "Optional briefing voice on Spec recompile",
                    },
                },
                "required": ["miz_path", "weather"],
            },
        },
    },
]


MUTATING_TOOL_NAMES: frozenset[str] = frozenset(
    {
        "compile_mission",
        "reweather_mission",
        "set_user_prefs",
        "record_generation",
        "record_feedback",
    }
)

# Host/CLI only during invent — burns turns on fake paths for vague asks.
INVENT_EXCLUDED_TOOL_NAMES: frozenset[str] = frozenset({"randomize_mission"})

# Full catalog (planning + mutating) for admin/tests; default agent surface is planning-only.
ALL_TOOL_DEFINITIONS: list[dict[str, Any]] = list(TOOL_DEFINITIONS)
TOOL_DEFINITIONS = [
    t
    for t in ALL_TOOL_DEFINITIONS
    if t["function"]["name"] not in MUTATING_TOOL_NAMES
    and t["function"]["name"] not in INVENT_EXCLUDED_TOOL_NAMES
]
MUTATING_TOOL_DEFINITIONS: list[dict[str, Any]] = [
    t for t in ALL_TOOL_DEFINITIONS if t["function"]["name"] in MUTATING_TOOL_NAMES
]


def dispatch_tool(
    name: str,
    arguments: dict[str, Any] | str,
    *,
    db_path: Path | str | None = None,
    allow_mutating: bool = False,
) -> dict[str, Any]:
    """Invoke a real tool by name; return its structured result dict.

    Mutating tools are blocked unless ``allow_mutating`` is True (host/tests only).
    """
    if isinstance(arguments, str):
        arguments = json.loads(arguments) if arguments.strip() else {}
    args = dict(arguments or {})

    if name in MUTATING_TOOL_NAMES and not allow_mutating:
        return {
            "ok": False,
            "error": (
                f"Tool {name!r} is host-owned (not on the default agent surface). "
                "Use CLI / host slash commands, or allow_mutating for tests."
            ),
            "code": "mutating_tool_blocked",
        }

    if name == "find_airfield":
        return find_airfield(str(args.get("query", "")), db_path=db_path)
    if name == "get_aircraft_details":
        return get_aircraft_details(str(args.get("aircraft_id", "")), db_path=db_path)
    if name == "list_mission_options":
        theatre = args.get("theatre")
        return list_mission_options(
            theatre=str(theatre) if theatre else None,
            db_path=db_path,
        )
    if name == "list_strike_targets":
        return list_strike_targets(
            domain=args.get("domain"),
            class_id=args.get("class_id"),
            q=args.get("q"),
            theatre=args.get("theatre"),
            db_path=db_path,
        )
    if name == "list_installed_campaigns":
        include_doc_text = bool(args.get("include_doc_text", False))
        return list_installed_campaigns(db_path=db_path, include_doc_text=include_doc_text)
    if name == "get_mission_spec_schema":
        theatre = args.get("theatre")
        return get_mission_spec_schema(
            str(args.get("mission_type", "")),
            theatre=str(theatre) if theatre else None,
        )
    if name == "get_user_prefs":
        keys = args.get("keys")
        if keys is not None and not isinstance(keys, list):
            keys = None
        return get_user_prefs(keys, db_path=db_path)
    if name == "set_user_prefs":
        prefs = args.get("prefs")
        if isinstance(prefs, dict):
            return set_user_prefs(prefs, db_path=db_path)
        # Flat kwargs without nested prefs object.
        flat = {k: v for k, v in args.items() if k != "prefs"}
        return set_user_prefs(flat or None, db_path=db_path)
    if name == "list_generation_history":
        limit = int(args.get("limit", 20) or 20)
        return list_generation_history(limit, db_path=db_path)
    if name == "record_generation":
        detail = args.get("detail")
        if detail is not None and not isinstance(detail, dict):
            detail = None
        return record_generation(
            outcome=str(args.get("outcome", "")),
            prompt=args.get("prompt"),
            mission_type=args.get("mission_type"),
            theatre=args.get("theatre"),
            spec_path=args.get("spec_path"),
            miz_path=args.get("miz_path"),
            detail=detail,
            db_path=db_path,
        )
    if name == "record_feedback":
        tags = args.get("tags")
        if tags is not None and not isinstance(tags, list):
            tags = None
        gid = args.get("generation_id")
        score = args.get("score")
        return record_feedback(
            source=str(args.get("source", "agent")),
            generation_id=int(gid) if gid is not None else None,
            score=int(score) if score is not None else None,
            note=args.get("note"),
            tags=tags,
            db_path=db_path,
        )
    if name == "research_guidance":
        return research_guidance(
            str(args.get("query", "")),
            mission_type=args.get("mission_type"),
            theatre=args.get("theatre"),
            aircraft=args.get("aircraft"),
            focus=args.get("focus"),
            db_path=db_path,
        )
    if name == "validate_mission_spec":
        return validate_mission_spec(str(args.get("spec_path", "")), db_path=db_path)
    if name == "compile_mission":
        return compile_mission(
            str(args.get("spec_path", "")),
            str(args.get("output_path", "")),
            db_path=db_path,
            voice=args.get("voice"),
        )
    if name == "reweather_mission":
        seed = args.get("seed")
        return reweather_mission_file(
            str(args.get("miz_path", "")),
            str(args.get("weather", "")),
            seed=int(seed) if seed is not None else None,
            spec_path=args.get("spec_path"),
            voice=args.get("voice"),
            db_path=db_path,
        )
    if name == "randomize_mission":
        axes = args.get("axes")
        return randomize_mission(
            seed=int(args.get("seed", -1)),
            spec_path=args.get("spec_path"),
            spec=args.get("spec") if isinstance(args.get("spec"), dict) else None,
            axes=axes if isinstance(axes, (list, str)) or axes is None else None,
            annotate=bool(args.get("annotate", False)),
            db_path=db_path,
        )
    return {"ok": False, "error": f"Unknown tool: {name}", "code": "unknown_tool"}
