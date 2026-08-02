"""Derived Mission Spec schema helper and tool."""

from __future__ import annotations

from dcs_miz_planner.agent.spec_schema import (
    build_spec_schema,
    infer_mission_type,
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
        build_spec_schema("escort")
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_infer_mission_type_from_rejected_json() -> None:
    assert infer_mission_type('{"mission_type": "cap", "theatre": "TheChannel"}') == "cap"
    assert infer_mission_type("no json here") == "free_flight"


def test_get_mission_spec_schema_tool() -> None:
    for mt in ("free_flight", "intercept", "cap", "ground_attack"):
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
