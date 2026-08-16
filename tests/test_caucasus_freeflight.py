"""Caucasus Batumi cold freeflight smoke (no CAP)."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    CAUCASUS_EXAMPLE_SPEC,
    CAUCASUS_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_batumi,
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
