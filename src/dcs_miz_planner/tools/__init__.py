"""Stable agent tool surface — import tools from here."""

from __future__ import annotations

from .surface import (
    compile_mission,
    find_airfield,
    get_aircraft_details,
    get_mission_spec_schema,
    get_user_prefs,
    list_generation_history,
    list_installed_campaigns,
    list_mission_options,
    randomize_mission,
    record_feedback,
    record_generation,
    research_guidance,
    set_user_prefs,
    validate_mission_spec,
)

__all__ = [
    "compile_mission",
    "find_airfield",
    "get_aircraft_details",
    "get_mission_spec_schema",
    "get_user_prefs",
    "list_generation_history",
    "list_installed_campaigns",
    "list_mission_options",
    "randomize_mission",
    "record_feedback",
    "record_generation",
    "research_guidance",
    "set_user_prefs",
    "validate_mission_spec",
]
