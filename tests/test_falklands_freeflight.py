"""Falklands Mount Pleasant cold freeflight smoke (no CAP)."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    FALKLANDS_EXAMPLE_SPEC,
    FALKLANDS_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_mount_pleasant,
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
