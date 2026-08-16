"""Syria Incirlik cold freeflight smoke (no CAP)."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    REQUIRED_MEMBERS,
    SYRIA_EXAMPLE_SPEC,
    SYRIA_MISSION_CONTRACTS,
    channel_available_inventory,
    compile_incirlik,
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
