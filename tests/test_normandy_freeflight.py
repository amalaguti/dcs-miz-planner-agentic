"""Normandy Needs Oar Point cold freeflight smoke."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    NORMANDY_CAP_EXAMPLE_SPEC,
    NORMANDY_CAP_MISSION_CONTRACTS,
    NORMANDY_ESCORT_EXAMPLE_SPEC,
    NORMANDY_ESCORT_MISSION_CONTRACTS,
    NORMANDY_EXAMPLE_SPEC,
    NORMANDY_GA_EXAMPLE_SPEC,
    NORMANDY_GA_MISSION_CONTRACTS,
    NORMANDY_INTERCEPT_EXAMPLE_SPEC,
    NORMANDY_INTERCEPT_MISSION_CONTRACTS,
    NORMANDY_MISSION_CONTRACTS,
    NORMANDY_RECON_EXAMPLE_SPEC,
    NORMANDY_RECON_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_needs_oar_point,
    compile_needs_oar_point_cap,
    compile_needs_oar_point_escort,
    compile_needs_oar_point_ground_attack,
    compile_needs_oar_point_intercept,
    compile_needs_oar_point_recon,
)

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.theatre_terrain import bound_theatre_ids, terrain_for_theatre
from dcs_miz_planner.validation import validate_mission_spec


def test_normandy_terrain_binds() -> None:
    terrain = terrain_for_theatre("Normandy")
    assert terrain.__class__.__name__ == "Normandy"
    assert "Normandy" in bound_theatre_ids()


def test_validate_needs_oar_point() -> None:
    spec = load_mission_spec(NORMANDY_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_needs_oar_point_contracts(tmp_path: Path) -> None:
    out = compile_needs_oar_point(tmp_path / "needs_oar_point.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Normandy" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NORMANDY_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_needs_oar_point_cap() -> None:
    spec = load_mission_spec(NORMANDY_CAP_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_needs_oar_point_cap_contracts(tmp_path: Path) -> None:
    out = compile_needs_oar_point_cap(tmp_path / "needs_oar_point_cap.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Normandy" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NORMANDY_CAP_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_needs_oar_point_ground_attack() -> None:
    spec = load_mission_spec(NORMANDY_GA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_needs_oar_point_ground_attack_contracts(tmp_path: Path) -> None:
    out = compile_needs_oar_point_ground_attack(tmp_path / "needs_oar_point_ga.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Normandy" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NORMANDY_GA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_needs_oar_point_intercept() -> None:
    spec = load_mission_spec(NORMANDY_INTERCEPT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_needs_oar_point_intercept_contracts(tmp_path: Path) -> None:
    out = compile_needs_oar_point_intercept(tmp_path / "needs_oar_point_intercept.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Normandy" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NORMANDY_INTERCEPT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_needs_oar_point_escort() -> None:
    spec = load_mission_spec(NORMANDY_ESCORT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_needs_oar_point_escort_contracts(tmp_path: Path) -> None:
    out = compile_needs_oar_point_escort(tmp_path / "needs_oar_point_escort.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Normandy" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NORMANDY_ESCORT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_needs_oar_point_recon() -> None:
    spec = load_mission_spec(NORMANDY_RECON_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_needs_oar_point_recon_contracts(tmp_path: Path) -> None:
    out = compile_needs_oar_point_recon(tmp_path / "needs_oar_point_recon.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Normandy" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NORMANDY_RECON_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
