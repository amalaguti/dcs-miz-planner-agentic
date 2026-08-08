"""Host invent path clamp (#8g)."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent.immersion import host_harbour_unit_nudge
from dcs_miz_planner.agent.path_clamp import (
    clamp_land_paths,
    land_path_deltas_from_registry,
    try_clamp_after_path_domain_fail,
)
from dcs_miz_planner.agent.prompts import host_spec_repair_nudge
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import GroundTarget, TargetMotion, TargetPathPoint
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
CONVOY = ROOT / "examples" / "manston_ground_attack_convoy.yaml"


def test_french_coast_path_deltas_from_registry() -> None:
    deltas = land_path_deltas_from_registry()
    assert len(deltas) >= 2
    assert deltas[0] == (0.0, 0.0)


def test_clamp_rewrites_mid_channel_land_path() -> None:
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
                        TargetPathPoint(bearing_deg=140, distance_km=40),
                        TargetPathPoint(bearing_deg=145, distance_km=42),
                        TargetPathPoint(bearing_deg=135, distance_km=38),
                    ],
                    ai_preset="convoy_transit",
                )
            ]
        }
    )
    failed = validate_mission_spec(bad, inventory=inv)
    assert not failed.ok
    assert any(e.code == "motion_domain_mismatch" for e in failed.errors)

    clamped = try_clamp_after_path_domain_fail(bad, list(failed.errors))
    assert clamped is not None
    ok = validate_mission_spec(clamped, inventory=inv)
    assert ok.ok, ok.errors
    path = clamped.targets[0].path
    assert len(path) == 3
    assert path[0].bearing_deg == 125
    assert path[0].distance_km == 76


def test_cli_style_validate_does_not_auto_clamp() -> None:
    """Author Specs stay unclamped — only invent/chat call try_clamp_*."""
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
                        TargetPathPoint(bearing_deg=140, distance_km=40),
                        TargetPathPoint(bearing_deg=145, distance_km=42),
                    ],
                    ai_preset="convoy_transit",
                )
            ]
        }
    )
    # Plain validate (CLI path) still fails — no side effect.
    result = validate_mission_spec(bad, inventory=inv)
    assert not result.ok
    unchanged, changed = clamp_land_paths(bad)
    assert changed
    # Original bad Spec object not mutated by clamp helper.
    assert bad.targets[0].path[0].distance_km == 40
    assert unchanged.targets[0].path[0].distance_km == 76


def test_repair_nudge_includes_path_yaml_example() -> None:
    payload = (
        'Validation failed:\n[{"code": "motion_domain_mismatch", '
        '"message": "Target Blitz is domain land but motion sample path[0] is sea"}]'
    )
    nudge = host_spec_repair_nudge(payload, mission_type="ground_attack")
    assert "bearing_deg: 125" in nudge or "125" in nudge
    assert "path:" in nudge
    assert "list_strike_targets(domain=sea)" in nudge or "domain=sea" in nudge


def test_harbour_unit_nudge_for_land_trucks() -> None:
    spec = load_mission_spec(CONVOY)
    nudge = host_harbour_unit_nudge("GA on harbour dock shipping at Dunkirk", spec)
    assert nudge is not None
    assert "domain=sea" in nudge
    assert "coastal_harbour" in nudge
    assert host_harbour_unit_nudge("inland truck convoy near Dunkirk", spec) is None
