"""Caucasus Batumi smoke (free_flight, CAP, GA, intercept)."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    BATUMI_CAP_EXAMPLE_SPEC,
    BATUMI_CAP_MISSION_CONTRACTS,
    BATUMI_GA_EXAMPLE_SPEC,
    BATUMI_GA_MISSION_CONTRACTS,
    BATUMI_INTERCEPT_EXAMPLE_SPEC,
    BATUMI_INTERCEPT_MISSION_CONTRACTS,
    BATUMI_SPITFIRE_EXAMPLE_SPEC,
    BATUMI_SPITFIRE_MISSION_CONTRACTS,
    CAUCASUS_EXAMPLE_SPEC,
    CAUCASUS_MISSION_CONTRACTS,
    MOZDOK_EXAMPLE_SPEC,
    MOZDOK_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_batumi,
    compile_batumi_cap,
    compile_batumi_ground_attack,
    compile_batumi_intercept,
    compile_batumi_spitfire,
    compile_mozdok,
)

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.theatre_terrain import bound_theatre_ids, terrain_for_theatre
from dcs_miz_planner.validation import validate_mission_spec


def test_caucasus_terrain_binds() -> None:
    terrain = terrain_for_theatre("Caucasus")
    assert terrain.__class__.__name__ == "Caucasus"
    assert "Caucasus" in bound_theatre_ids()


def test_validate_batumi() -> None:
    spec = load_mission_spec(CAUCASUS_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_batumi_contracts(tmp_path: Path) -> None:
    out = compile_batumi(tmp_path / "batumi.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Caucasus" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in CAUCASUS_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_mozdok() -> None:
    spec = load_mission_spec(MOZDOK_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_mozdok_contracts(tmp_path: Path) -> None:
    out = compile_mozdok(tmp_path / "mozdok.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Caucasus" in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in MOZDOK_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"


def test_validate_batumi_spitfire() -> None:
    spec = load_mission_spec(BATUMI_SPITFIRE_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_batumi_spitfire_contracts(tmp_path: Path) -> None:
    out = compile_batumi_spitfire(tmp_path / "batumi_spitfire.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Caucasus" in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in BATUMI_SPITFIRE_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        # Player unit type — not a whole-file substring: PyDCS requiredModules
        # still lists "Su-25T by Eagle Dynamics" even when the player is a Spitfire.
        assert '["type"]="SpitfireLFMkIX"' in mission
        assert '["type"]="Su-25T"' not in mission


def test_validate_batumi_cap() -> None:
    spec = load_mission_spec(BATUMI_CAP_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_batumi_cap_contracts(tmp_path: Path) -> None:
    out = compile_batumi_cap(tmp_path / "batumi_cap.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Caucasus" in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in BATUMI_CAP_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_batumi_ground_attack() -> None:
    spec = load_mission_spec(BATUMI_GA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_batumi_ground_attack_contracts(tmp_path: Path) -> None:
    out = compile_batumi_ground_attack(tmp_path / "batumi_ga.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Caucasus" in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in BATUMI_GA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "Blitz_36-6700A" not in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_validate_batumi_intercept() -> None:
    spec = load_mission_spec(BATUMI_INTERCEPT_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_batumi_intercept_contracts(tmp_path: Path) -> None:
    out = compile_batumi_intercept(tmp_path / "batumi_intercept.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Caucasus" in theatre
        assert "Normandy" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in BATUMI_INTERCEPT_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission
        assert "78296.390625" not in mission
