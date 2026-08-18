"""Nevada Nellis / Groom Lake cold freeflight, north-range CAP, intercept, escort, and GA smoke."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    GROOM_LAKE_EXAMPLE_SPEC,
    GROOM_LAKE_MISSION_CONTRACTS,
    NEVADA_CAP_EXAMPLE_SPEC,
    NEVADA_CAP_MISSION_CONTRACTS,
    NEVADA_ESCORT_EXAMPLE_SPEC,
    NEVADA_ESCORT_MISSION_CONTRACTS,
    NEVADA_EXAMPLE_SPEC,
    NEVADA_GA_EXAMPLE_SPEC,
    NEVADA_GA_MISSION_CONTRACTS,
    NEVADA_INTERCEPT_EXAMPLE_SPEC,
    NEVADA_INTERCEPT_MISSION_CONTRACTS,
    NEVADA_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_groom_lake,
    compile_nellis,
    compile_nellis_cap,
    compile_nellis_escort,
    compile_nellis_ground_attack,
    compile_nellis_intercept,
)

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.theatre_terrain import bound_theatre_ids, terrain_for_theatre
from dcs_miz_planner.validation import validate_mission_spec


def test_nevada_terrain_binds() -> None:
    terrain = terrain_for_theatre("Nevada")
    assert terrain.__class__.__name__ == "Nevada"
    assert "Nevada" in bound_theatre_ids()


def test_validate_nellis() -> None:
    spec = load_mission_spec(NEVADA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_nellis_contracts(tmp_path: Path) -> None:
    out = compile_nellis(tmp_path / "nellis.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Nevada" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NEVADA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_nellis_cap() -> None:
    spec = load_mission_spec(NEVADA_CAP_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_nellis_cap_contracts(tmp_path: Path) -> None:
    out = compile_nellis_cap(tmp_path / "nellis_cap.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Nevada" in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NEVADA_CAP_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "ThirdReich" not in mission
        assert "181207.773438" not in mission
        assert "-35240.347656" not in mission
        assert "30989.935547" not in mission


def test_validate_nellis_intercept() -> None:
    spec = load_mission_spec(NEVADA_INTERCEPT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_nellis_intercept_contracts(tmp_path: Path) -> None:
    out = compile_nellis_intercept(tmp_path / "nellis_intercept.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Nevada" in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NEVADA_INTERCEPT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "USA" in mission
        assert "Russia" in mission
        assert "ThirdReich" not in mission
        assert "181207.773438" not in mission
        assert "-35240.347656" not in mission
        assert "30989.935547" not in mission


def test_validate_nellis_escort() -> None:
    spec = load_mission_spec(NEVADA_ESCORT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_nellis_escort_contracts(tmp_path: Path) -> None:
    out = compile_nellis_escort(tmp_path / "nellis_escort.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Nevada" in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NEVADA_ESCORT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "USA" in mission
        assert "Russia" in mission
        assert "ThirdReich" not in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "-358803.06487951166" in mission
        assert "-24179.16392267721" in mission
        assert "181207.773438" not in mission
        assert "-35240.347656" not in mission
        assert "30989.935547" not in mission


def test_validate_nellis_ground_attack() -> None:
    spec = load_mission_spec(NEVADA_GA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_nellis_ground_attack_contracts(tmp_path: Path) -> None:
    out = compile_nellis_ground_attack(tmp_path / "nellis_ga.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Nevada" in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in NEVADA_GA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "USA" in mission
        assert "Russia" in mission
        assert "ThirdReich" not in mission
        assert "Blitz_36-6700A" not in mission
        assert "-358803.06487951166" not in mission
        assert "-24179.16392267721" not in mission
        assert "Hawkinge" not in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_groom_lake() -> None:
    spec = load_mission_spec(GROOM_LAKE_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_groom_lake_contracts(tmp_path: Path) -> None:
    out = compile_groom_lake(tmp_path / "groom_lake.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Nevada" in theatre
        assert "Falklands" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in GROOM_LAKE_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
