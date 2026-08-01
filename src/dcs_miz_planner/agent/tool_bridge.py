"""Bridge OpenAI-style tool definitions to dcs_miz_planner.tools."""

from __future__ import annotations

import json
from typing import Any

from ..tools import (
    compile_mission,
    find_airfield,
    get_aircraft_details,
    list_mission_options,
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


def dispatch_tool(name: str, arguments: dict[str, Any] | str) -> dict[str, Any]:
    """Invoke a real tool by name; return its structured result dict."""
    if isinstance(arguments, str):
        arguments = json.loads(arguments) if arguments.strip() else {}
    args = arguments or {}

    if name == "find_airfield":
        return find_airfield(str(args.get("query", "")))
    if name == "get_aircraft_details":
        return get_aircraft_details(str(args.get("aircraft_id", "")))
    if name == "list_mission_options":
        return list_mission_options()
    if name == "validate_mission_spec":
        return validate_mission_spec(str(args.get("spec_path", "")))
    if name == "compile_mission":
        return compile_mission(
            str(args.get("spec_path", "")),
            str(args.get("output_path", "")),
        )
    return {"ok": False, "error": f"Unknown tool: {name}", "code": "unknown_tool"}
