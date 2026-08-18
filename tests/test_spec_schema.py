"""Derived Mission Spec schema helper and tool."""

from __future__ import annotations

from dcs_miz_planner.agent.spec_schema import (
    build_spec_schema,
    infer_mission_type,
    infer_theatre,
    supported_mission_types,
)
from dcs_miz_planner.agent.tool_bridge import TOOL_DEFINITIONS, dispatch_tool
from dcs_miz_planner.models import MissionSpec
from dcs_miz_planner.tools import get_mission_spec_schema


def test_supported_types_have_validating_examples() -> None:
    for mt in supported_mission_types():
        view = build_spec_schema(mt)
        assert view.mission_type == mt
        MissionSpec.model_validate(view.example)
        assert view.example["mission_type"] == mt
        assert "player" in view.example
        assert isinstance(view.example["date"], dict)


def test_unknown_mission_type_raises() -> None:
    try:
        build_spec_schema("not_a_real_mission_type")
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_infer_mission_type_from_rejected_json() -> None:
    assert infer_mission_type('{"mission_type": "cap", "theatre": "TheChannel"}') == "cap"
    assert infer_mission_type("no json here") == "free_flight"


def test_infer_theatre_from_rejected_json() -> None:
    assert infer_theatre('{"mission_type": "cap", "theatre": "Normandy"}') == "Normandy"
    assert infer_theatre('{"mission_type": "cap", "theatre": "TheChannel"}') == "TheChannel"
    assert infer_theatre('{"mission_type": "cap"}') is None
    assert infer_theatre("no json here") is None
    assert (
        infer_theatre('{"mission_type": "cap", "player": {"airfield": "NeedsOarPoint"}}')
        == "Normandy"
    )
    assert infer_theatre('{"mission_type": "free_flight", "theatre": "Caucasus"}') == "Caucasus"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Batumi"}}') == "Caucasus"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Mozdok"}}') == "Caucasus"
    assert infer_theatre('{"mission_type": "free_flight", "theatre": "Syria"}') == "Syria"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Incirlik"}}') == "Syria"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Palmyra"}}') == "Syria"
    assert infer_theatre('{"mission_type": "free_flight", "theatre": "Nevada"}') == "Nevada"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Nellis"}}') == "Nevada"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "GroomLake"}}') == "Nevada"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Creech"}}') == "Nevada"
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Groom_Lake"}}') is None
    assert infer_theatre('{"mission_type": "free_flight", "theatre": "Falklands"}') == "Falklands"
    assert (
        infer_theatre('{"mission_type": "cap", "player": {"airfield": "MountPleasant"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "cap", "player": {"airfield": "Mount_Pleasant"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "RioGallegos"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "PortStanley"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "SanCarlosFOB"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "RioGrande"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "Ushuaia"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "PuntaArenas"}}')
        == "Falklands"
    )
    assert (
        infer_theatre('{"mission_type": "free_flight", "player": {"airfield": "SanJulian"}}')
        == "Falklands"
    )
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Rio_Gallegos"}}') is None
    assert infer_theatre('{"mission_type": "cap", "player": {"airfield": "Port_Stanley"}}') is None


def test_get_mission_spec_schema_tool() -> None:
    for mt in ("free_flight", "intercept", "cap", "ground_attack", "escort"):
        result = get_mission_spec_schema(mt)
        assert result["ok"] is True
        assert result["mission_type"] == mt
        MissionSpec.model_validate(result["example"])
        assert result["notes"]
        assert result["anti_patterns"]


def test_get_mission_spec_schema_unknown() -> None:
    result = get_mission_spec_schema("not_a_type")
    assert result["ok"] is False
    assert result["code"] == "unsupported_mission_type"


def test_bridge_lists_and_dispatches_schema_tool() -> None:
    names = {t["function"]["name"] for t in TOOL_DEFINITIONS}
    assert "get_mission_spec_schema" in names
    out = dispatch_tool("get_mission_spec_schema", {"mission_type": "cap"})
    assert out["ok"] is True
    assert out["example"]["mission_type"] == "cap"
