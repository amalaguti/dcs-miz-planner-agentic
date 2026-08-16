"""Soft immersion floor cues and host nudge."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent.immersion import (
    host_immersion_repair_nudge,
    immersion_cues,
    immersion_gap,
)
from dcs_miz_planner.agent.llm import StubLLM
from dcs_miz_planner.agent.planner import plan_mission
from dcs_miz_planner.agent.spec_schema import build_spec_schema
from dcs_miz_planner.agent.tool_bridge import TOOL_DEFINITIONS
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import MissionSpec


def test_cues_interesting_and_campaign() -> None:
    cues = immersion_cues("interesting free flight from Manston")
    assert any(c[0] == "altitude_speed_gates" for c in cues)
    cues2 = immersion_cues("something like a Big Show style sortie")
    assert any(c[0] == "radio_late_activation" for c in cues2)


def test_gap_bare_freeflight() -> None:
    bare = MissionSpec.model_validate(
        {
            "schema_version": "1",
            "mission_type": "free_flight",
            "theatre": "TheChannel",
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
        }
    )
    gap = immersion_gap("interesting free flight", bare)
    assert gap is not None
    assert gap[0] == "altitude_speed_gates"
    assert host_immersion_repair_nudge("interesting free flight", bare)


def test_immersion_nudge_skipped_off_channel() -> None:
    syria = MissionSpec.model_validate(
        {
            "schema_version": "1",
            "mission_type": "free_flight",
            "theatre": "Syria",
            "date": {"year": 2024, "month": 6, "day": 6},
            "start_time": "09:00",
            "weather": "sunny_clear",
            "player": {
                "aircraft": "Su-25T",
                "airfield": "Incirlik",
                "coalition": "blue",
                "country": "Turkey",
                "skill": "Player",
                "start": "cold_parking",
            },
        }
    )
    nudge = host_immersion_repair_nudge("interesting free flight", syria)
    assert nudge is None


def test_no_gap_when_gates_present() -> None:
    gates = load_mission_spec(Path("examples/manston_freeflight_altitude_speed_gates.yaml"))
    assert immersion_gap("interesting free flight", gates) is None


def test_free_flight_schema_prefers_gates() -> None:
    view = build_spec_schema("free_flight")
    blob = str(view.example)
    assert "unit_altitude" in blob or "unit_speed" in blob


def test_default_tools_exclude_randomize() -> None:
    names = {t["function"]["name"] for t in TOOL_DEFINITIONS}
    assert "randomize_mission" not in names
    assert "list_mission_options" in names


def test_plan_nudges_then_accepts_bare(tmp_path: Path) -> None:
    """Stub returns bare Spec twice; host nudges once then accepts (soft floor)."""
    bare = (
        '{"schema_version":"1","mission_type":"free_flight","theatre":"TheChannel",'
        '"date":{"year":1944,"month":6,"day":6},"start_time":"09:00",'
        '"weather":"sunny_clear","player":{"aircraft":"SpitfireLFMkIX",'
        '"airfield":"Manston","coalition":"blue","country":"UK","skill":"Player",'
        '"start":"cold_parking"},"enemies":[],"objectives":[],"triggers":[]}'
    )
    from dcs_miz_planner.agent.llm import LLMResponse

    llm = StubLLM(script=[LLMResponse(content=bare), LLMResponse(content=bare)])
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "interesting free flight from Manston",
        out,
        llm=llm,
        inventory=channel_available_inventory(),
        db_path=tmp_path / "db.sqlite",
        max_turns=4,
    )
    assert result.ok
    assert out.is_file()
    # Soft floor: accepted bare after one nudge (script had no gates).
    spec = load_mission_spec(out)
    assert spec.mission_type.value == "free_flight"
