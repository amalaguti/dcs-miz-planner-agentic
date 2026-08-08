"""Target AI options (#15h) — presets, class allowlists, compile evidence."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory
from pydantic import ValidationError

from dcs_miz_planner.compiler.pydcs_compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import (
    GroundTarget,
    TargetAi,
    TargetAlarmState,
    TargetMotion,
    TargetMoveFormation,
    TargetPathPoint,
    TargetRoe,
)
from dcs_miz_planner.target_ai import resolve_target_ai, target_ai_class
from dcs_miz_planner.validation import validate_mission_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
CONVOY = REPO_ROOT / "examples" / "manston_ground_attack_convoy.yaml"
UBOAT_HUNT = REPO_ROOT / "examples" / "manston_uboat_hunt.yaml"
FLAK = REPO_ROOT / "examples" / "manston_ground_attack_flak_alert.yaml"


def test_unknown_ai_preset_rejected() -> None:
    with pytest.raises(ValidationError, match="ai_preset"):
        GroundTarget(unit="Blitz_36-6700A", count=1, ai_preset="not_a_real_preset")


def test_omit_ai_ok() -> None:
    tgt = GroundTarget(unit="Blitz_36-6700A", count=1)
    assert resolve_target_ai(tgt).has_emit() is False


def test_convoy_preset_resolves() -> None:
    tgt = GroundTarget(unit="Blitz_36-6700A", count=1, ai_preset="convoy_transit")
    r = resolve_target_ai(tgt)
    assert r.alarm_state is TargetAlarmState.GREEN
    assert r.roe is TargetRoe.RETURN_FIRE
    assert r.move_formation is TargetMoveFormation.OFF_ROAD


def test_explicit_overrides_preset() -> None:
    tgt = GroundTarget(
        unit="Blitz_36-6700A",
        count=1,
        ai_preset="convoy_transit",
        ai=TargetAi(alarm_state=TargetAlarmState.RED),
        move_formation=TargetMoveFormation.ON_ROAD,
    )
    r = resolve_target_ai(tgt)
    assert r.alarm_state is TargetAlarmState.RED
    assert r.move_formation is TargetMoveFormation.ON_ROAD
    assert r.roe is TargetRoe.RETURN_FIRE


def test_soft_truck_interception_rejected() -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(CONVOY)
    bad = spec.model_copy(
        update={
            "targets": [
                GroundTarget(
                    unit="Blitz_36-6700A",
                    count=3,
                    motion=TargetMotion.PATH,
                    path=[
                        TargetPathPoint(bearing_deg=125, distance_km=76),
                        TargetPathPoint(bearing_deg=128, distance_km=77),
                    ],
                    ai=TargetAi(interception_range=50),
                )
            ]
        }
    )
    result = validate_mission_spec(bad, inventory=inv)
    assert not result.ok
    assert any(e.code == "target_ai_class_mismatch" for e in result.errors)


def test_sea_move_formation_rejected() -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(UBOAT_HUNT)
    bad = spec.model_copy(
        update={
            "targets": [
                GroundTarget(
                    unit="Uboat_VIIC",
                    count=1,
                    motion=TargetMotion.PATROL,
                    patrol_radius_m=2500,
                    move_formation=TargetMoveFormation.ON_ROAD,
                )
            ]
        }
    )
    result = validate_mission_spec(bad, inventory=inv)
    assert not result.ok
    assert any(e.code == "target_ai_class_mismatch" for e in result.errors)


def test_flak_interception_accepted() -> None:
    assert target_ai_class("flak18", domain="land") == "aaa"
    inv = channel_available_inventory()
    spec = load_mission_spec(FLAK)
    result = validate_mission_spec(spec, inventory=inv)
    assert result.ok, result.errors


def test_convoy_ai_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(CONVOY)
    assert spec.targets[0].ai_preset == "convoy_transit"
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "convoy_ai.miz", voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    compact = mission.replace(" ", "")
    assert "Blitz_36-6700A" in mission
    assert "Off Road" in mission
    # OptROE ReturnFire=3, OptAlarmState Green=1
    assert '["name"]=0' in compact
    assert '["value"]=3' in compact
    assert '["name"]=9' in compact
    assert '["value"]=1' in compact


def test_uboat_ai_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(UBOAT_HUNT)
    assert spec.targets[0].ai_preset == "ship_under_way" or spec.targets[0].ai is not None
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "uboat_ai.miz", voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    compact = mission.replace(" ", "")
    assert "Uboat_VIIC" in mission
    assert '["name"]=9' in compact


def test_flak_alert_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(FLAK)
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "flak.miz", voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    compact = mission.replace(" ", "")
    assert "flak18" in mission
    assert '["name"]=9' in compact
    assert '["name"]=24' in compact
