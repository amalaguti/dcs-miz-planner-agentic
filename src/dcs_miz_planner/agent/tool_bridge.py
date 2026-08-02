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
    list_mission_options,
    record_feedback,
    record_generation,
    research_guidance,
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
                "options with support levels (supported|advisory|future)."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_mission_spec_schema",
            "description": (
                "Get a compact Mission Spec JSON example plus notes/anti-patterns for a "
                "mission_type (free_flight, intercept, cap, or ground_attack). "
                "Call before emitting Spec JSON."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "mission_type": {
                        "type": "string",
                        "description": "free_flight | intercept | cap | ground_attack",
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
            "description": "List recent mission generations (newest first).",
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
                "explicitly logging an attempt."
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
                    "detail": {"type": "object"},
                },
                "required": ["outcome"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_feedback",
            "description": "Record satisfaction feedback (score/note/tags).",
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
                "pilot accounts, or historical context for the commander brief. "
                "Not a source of DCS type ids or Spec fields."
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
            "description": "Compile a Mission Spec YAML to a .miz file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spec_path": {"type": "string"},
                    "output_path": {"type": "string"},
                },
                "required": ["spec_path", "output_path"],
            },
        },
    },
]


def dispatch_tool(
    name: str,
    arguments: dict[str, Any] | str,
    *,
    db_path: Path | str | None = None,
) -> dict[str, Any]:
    """Invoke a real tool by name; return its structured result dict."""
    if isinstance(arguments, str):
        arguments = json.loads(arguments) if arguments.strip() else {}
    args = dict(arguments or {})

    if name == "find_airfield":
        return find_airfield(str(args.get("query", "")), db_path=db_path)
    if name == "get_aircraft_details":
        return get_aircraft_details(str(args.get("aircraft_id", "")), db_path=db_path)
    if name == "list_mission_options":
        return list_mission_options(db_path=db_path)
    if name == "get_mission_spec_schema":
        return get_mission_spec_schema(str(args.get("mission_type", "")))
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
            db_path=db_path,
        )
    if name == "validate_mission_spec":
        return validate_mission_spec(str(args.get("spec_path", "")), db_path=db_path)
    if name == "compile_mission":
        return compile_mission(
            str(args.get("spec_path", "")),
            str(args.get("output_path", "")),
            db_path=db_path,
        )
    return {"ok": False, "error": f"Unknown tool: {name}", "code": "unknown_tool"}
