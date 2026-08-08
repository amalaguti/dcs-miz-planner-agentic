"""Target motion (patrol / path) on GA and recon contacts."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory
from pydantic import ValidationError

from dcs_miz_planner.compiler.pydcs_compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import GroundTarget, TargetMotion, TargetPathPoint
from dcs_miz_planner.validation import validate_mission_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
UBOAT_RECON = REPO_ROOT / "examples" / "manston_uboat_recon.yaml"
UBOAT_HUNT = REPO_ROOT / "examples" / "manston_uboat_hunt.yaml"
CONVOY = REPO_ROOT / "examples" / "manston_ground_attack_convoy.yaml"


def test_ground_target_static_rejects_path_fields() -> None:
    with pytest.raises(ValidationError, match="(?i)path"):
        GroundTarget(
            unit="Blitz_36-6700A",
            count=1,
            path=[TargetPathPoint(bearing_deg=1, distance_km=1)],
        )


def test_ground_target_patrol_requires_radius() -> None:
    with pytest.raises(ValidationError, match="(?i)patrol_radius"):
        GroundTarget(unit="Uboat_VIIC", count=1, motion=TargetMotion.PATROL)


def test_uboat_patrol_validates(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    for path in (UBOAT_RECON, UBOAT_HUNT):
        spec = load_mission_spec(path)
        result = validate_mission_spec(spec, inventory=inv)
        assert result.ok, result.errors
        assert spec.targets[0].motion is TargetMotion.PATROL


def test_sea_path_on_land_rejected() -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(UBOAT_HUNT)
    bad = spec.model_copy(
        update={
            "targets": [
                GroundTarget(
                    unit="Uboat_VIIC",
                    count=1,
                    motion=TargetMotion.PATH,
                    path=[
                        TargetPathPoint(bearing_deg=125, distance_km=76),
                        TargetPathPoint(bearing_deg=128, distance_km=77),
                    ],
                )
            ]
        }
    )
    result = validate_mission_spec(bad, inventory=inv)
    assert not result.ok
    assert any(e.code == "motion_domain_mismatch" for e in result.errors)


def test_convoy_path_validates_and_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(CONVOY)
    result = validate_mission_spec(spec, inventory=inv)
    assert result.ok, result.errors
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "convoy.miz", voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert "Blitz_36-6700A" in mission
    assert "SwitchWaypoint" in mission
    # Multi-point route (more than a single spawn point).
    assert mission.count('["type"] = "Turning Point"') >= 2 or mission.count("Turning Point") >= 2


def test_uboat_patrol_compiles_with_switch_waypoint(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(UBOAT_RECON)
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "uboat_patrol.miz", voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert "Uboat_VIIC" in mission
    assert "SwitchWaypoint" in mission
    assert "Reconnaissance" in mission
    assert "Bombing" not in mission


def test_speed_profile_bands_and_seeded_cruise() -> None:
    from dcs_miz_planner.target_motion import (
        resolve_cruise_kmh,
        speed_profile_for_unit,
        waypoint_speeds_kmh,
    )

    soft = speed_profile_for_unit("Blitz_36-6700A", domain="land")
    assert soft.min_kmh < soft.max_kmh
    uboat = speed_profile_for_unit("Uboat_VIIC", domain="sea")
    assert uboat.max_kmh < soft.max_kmh  # surfaced sub slower than truck top band

    tgt = GroundTarget(
        unit="Blitz_36-6700A",
        count=3,
        motion=TargetMotion.PATH,
        path=[
            TargetPathPoint(bearing_deg=125, distance_km=76),
            TargetPathPoint(bearing_deg=128, distance_km=77),
        ],
    )
    a = resolve_cruise_kmh(tgt, domain="land", seed=42, target_index=0)
    b = resolve_cruise_kmh(tgt, domain="land", seed=42, target_index=0)
    c = resolve_cruise_kmh(tgt, domain="land", seed=99, target_index=0)
    assert a == b
    assert soft.min_kmh <= a <= soft.max_kmh
    assert soft.min_kmh <= c <= soft.max_kmh
    speeds = waypoint_speeds_kmh(a, count=3, seed=42, target_index=0)
    assert len(speeds) == 3
    assert len({round(s, 1) for s in speeds}) >= 2  # within-mission variation


def test_disperse_under_fire_land_moving_default_sea_off() -> None:
    from dcs_miz_planner.target_motion import resolve_disperse_under_fire_s

    truck = GroundTarget(
        unit="Blitz_36-6700A",
        count=3,
        motion=TargetMotion.PATH,
        path=[
            TargetPathPoint(bearing_deg=125, distance_km=76),
            TargetPathPoint(bearing_deg=128, distance_km=77),
        ],
    )
    assert resolve_disperse_under_fire_s(truck, domain="land") == 180
    assert (
        resolve_disperse_under_fire_s(
            truck.model_copy(update={"disperse_under_fire_s": 0}), domain="land"
        )
        is None
    )
    assert (
        resolve_disperse_under_fire_s(
            truck.model_copy(update={"disperse_under_fire_s": 90}), domain="land"
        )
        == 90
    )

    boat = GroundTarget(
        unit="Uboat_VIIC",
        count=1,
        motion=TargetMotion.PATROL,
        patrol_radius_m=2000,
    )
    assert resolve_disperse_under_fire_s(boat, domain="sea") is None


def test_convoy_compiles_disperse_under_fire(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(CONVOY)
    out = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "convoy_disp.miz", voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert "Blitz_36-6700A" in mission
    # OptDisparseUnderFire → Option name 8, value 180
    assert '["name"]=8' in mission.replace(" ", "") or '["name"] = 8' in mission
    assert "180" in mission


def test_speed_kmh_out_of_band_rejected() -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(CONVOY)
    bad = spec.model_copy(
        update={
            "targets": [
                GroundTarget(
                    unit="Blitz_36-6700A",
                    count=3,
                    motion=TargetMotion.PATH,
                    speed_kmh=100,
                    path=list(spec.targets[0].path),
                )
            ]
        }
    )
    result = validate_mission_spec(bad, inventory=inv)
    assert not result.ok
    assert any(e.code == "motion_speed_out_of_range" for e in result.errors)
