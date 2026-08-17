"""Syria Incirlik cold freeflight, Iskenderun CAP, escort, and Aleppo GA smoke."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    INCIRLIK_CAP_EXAMPLE_SPEC,
    INCIRLIK_CAP_MISSION_CONTRACTS,
    INCIRLIK_ESCORT_EXAMPLE_SPEC,
    INCIRLIK_ESCORT_MISSION_CONTRACTS,
    INCIRLIK_GA_EXAMPLE_SPEC,
    INCIRLIK_GA_MISSION_CONTRACTS,
    INCIRLIK_INTERCEPT_EXAMPLE_SPEC,
    INCIRLIK_INTERCEPT_MISSION_CONTRACTS,
    PALMYRA_EXAMPLE_SPEC,
    PALMYRA_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    SYRIA_EXAMPLE_SPEC,
    SYRIA_MISSION_CONTRACTS,
    channel_available_inventory,
    compile_incirlik,
    compile_incirlik_cap,
    compile_incirlik_escort,
    compile_incirlik_ground_attack,
    compile_incirlik_intercept,
    compile_palmyra,
)

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.theatre_terrain import bound_theatre_ids, terrain_for_theatre
from dcs_miz_planner.validation import validate_mission_spec


def test_syria_terrain_binds() -> None:
    terrain = terrain_for_theatre("Syria")
    assert terrain.__class__.__name__ == "Syria"
    assert "Syria" in bound_theatre_ids()


def test_validate_incirlik() -> None:
    spec = load_mission_spec(SYRIA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_incirlik_contracts(tmp_path: Path) -> None:
    out = compile_incirlik(tmp_path / "incirlik.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Syria" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in SYRIA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_palmyra() -> None:
    spec = load_mission_spec(PALMYRA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_palmyra_contracts(tmp_path: Path) -> None:
    out = compile_palmyra(tmp_path / "palmyra.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Syria" in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in PALMYRA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission


def test_validate_incirlik_cap() -> None:
    spec = load_mission_spec(INCIRLIK_CAP_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_incirlik_cap_contracts(tmp_path: Path) -> None:
    out = compile_incirlik_cap(tmp_path / "incirlik_cap.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Syria" in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in INCIRLIK_CAP_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_incirlik_intercept() -> None:
    spec = load_mission_spec(INCIRLIK_INTERCEPT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_incirlik_intercept_contracts(tmp_path: Path) -> None:
    out = compile_incirlik_intercept(tmp_path / "incirlik_intercept.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Syria" in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in INCIRLIK_INTERCEPT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_incirlik_escort() -> None:
    spec = load_mission_spec(INCIRLIK_ESCORT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_incirlik_escort_contracts(tmp_path: Path) -> None:
    out = compile_incirlik_escort(tmp_path / "incirlik_escort.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Syria" in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in INCIRLIK_ESCORT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_incirlik_ground_attack() -> None:
    spec = load_mission_spec(INCIRLIK_GA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_incirlik_ground_attack_contracts(tmp_path: Path) -> None:
    out = compile_incirlik_ground_attack(tmp_path / "incirlik_ga.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Syria" in theatre
        assert "Caucasus" not in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in INCIRLIK_GA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "Blitz_36-6700A" not in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission
