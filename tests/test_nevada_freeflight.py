"""Nevada Nellis / Groom Lake cold freeflight and Nellis north-range CAP smoke."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    GROOM_LAKE_EXAMPLE_SPEC,
    GROOM_LAKE_MISSION_CONTRACTS,
    NEVADA_CAP_EXAMPLE_SPEC,
    NEVADA_CAP_MISSION_CONTRACTS,
    NEVADA_EXAMPLE_SPEC,
    NEVADA_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_groom_lake,
    compile_nellis,
    compile_nellis_cap,
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
