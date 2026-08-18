"""Falklands Mount Pleasant cold freeflight, South Atlantic CAP, intercept, and escort smoke."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    FALKLANDS_CAP_EXAMPLE_SPEC,
    FALKLANDS_CAP_MISSION_CONTRACTS,
    FALKLANDS_ESCORT_EXAMPLE_SPEC,
    FALKLANDS_ESCORT_MISSION_CONTRACTS,
    FALKLANDS_EXAMPLE_SPEC,
    FALKLANDS_INTERCEPT_EXAMPLE_SPEC,
    FALKLANDS_INTERCEPT_MISSION_CONTRACTS,
    FALKLANDS_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    RIO_GALLEGOS_EXAMPLE_SPEC,
    RIO_GALLEGOS_MISSION_CONTRACTS,
    channel_available_inventory,
    compile_mount_pleasant,
    compile_mount_pleasant_cap,
    compile_mount_pleasant_escort,
    compile_mount_pleasant_intercept,
    compile_rio_gallegos,
)

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.theatre_terrain import bound_theatre_ids, terrain_for_theatre
from dcs_miz_planner.validation import validate_mission_spec


def test_falklands_terrain_binds() -> None:
    terrain = terrain_for_theatre("Falklands")
    assert terrain.__class__.__name__ == "Falklands"
    assert "Falklands" in bound_theatre_ids()


def test_validate_mount_pleasant() -> None:
    spec = load_mission_spec(FALKLANDS_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_mount_pleasant_contracts(tmp_path: Path) -> None:
    out = compile_mount_pleasant(tmp_path / "mount_pleasant.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Falklands" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in FALKLANDS_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_mount_pleasant_cap() -> None:
    spec = load_mission_spec(FALKLANDS_CAP_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_mount_pleasant_cap_contracts(tmp_path: Path) -> None:
    out = compile_mount_pleasant_cap(tmp_path / "mount_pleasant_cap.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Falklands" in theatre
        assert "Nevada" not in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in FALKLANDS_CAP_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "ThirdReich" not in mission
        assert "Chile" not in mission


def test_validate_mount_pleasant_intercept() -> None:
    spec = load_mission_spec(FALKLANDS_INTERCEPT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_mount_pleasant_intercept_contracts(tmp_path: Path) -> None:
    out = compile_mount_pleasant_intercept(tmp_path / "mount_pleasant_intercept.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Falklands" in theatre
        assert "Nevada" not in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in FALKLANDS_INTERCEPT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "UK" in mission
        assert "Argentina" in mission
        assert "ThirdReich" not in mission
        assert "Nellis" not in mission
        assert "Incirlik" not in mission
        assert "30989.935547" not in mission
        assert "-358803.06487951166" not in mission
        assert "181207.773438" not in mission


def test_validate_mount_pleasant_escort() -> None:
    spec = load_mission_spec(FALKLANDS_ESCORT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_mount_pleasant_escort_contracts(tmp_path: Path) -> None:
    out = compile_mount_pleasant_escort(tmp_path / "mount_pleasant_escort.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Falklands" in theatre
        assert "Nevada" not in theatre
        assert "Syria" not in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in FALKLANDS_ESCORT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert '["task"]="Escort"' in mission
        assert "UK" in mission
        assert "Argentina" in mission
        assert "ThirdReich" not in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "Nellis" not in mission
        assert "Incirlik" not in mission
        assert "30989.935547" not in mission
        assert "-358803.06487951166" not in mission
        assert "181207.773438" not in mission


def test_validate_rio_gallegos() -> None:
    spec = load_mission_spec(RIO_GALLEGOS_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_rio_gallegos_contracts(tmp_path: Path) -> None:
    out = compile_rio_gallegos(tmp_path / "rio_gallegos.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Falklands" in theatre
        assert "TheChannel" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in RIO_GALLEGOS_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "Argentina" in mission
