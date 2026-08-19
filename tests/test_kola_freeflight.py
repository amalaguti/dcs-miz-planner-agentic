"""Kola Bodo cold freeflight smoke."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    KOLA_EXAMPLE_SPEC,
    KOLA_MISSION_CONTRACTS,
    REQUIRED_MEMBERS,
    channel_available_inventory,
    compile_bodo,
)

from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.theatre_terrain import bound_theatre_ids, terrain_for_theatre
from dcs_miz_planner.validation import validate_mission_spec


def test_kola_terrain_binds() -> None:
    terrain = terrain_for_theatre("Kola")
    assert terrain.__class__.__name__ == "Kola"
    assert "Kola" in bound_theatre_ids()


def test_validate_bodo() -> None:
    spec = load_mission_spec(KOLA_EXAMPLE_SPEC)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_compile_bodo_contracts(tmp_path: Path) -> None:
    out = compile_bodo(tmp_path / "bodo.miz")
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        names = set(zf.namelist())
        for member in REQUIRED_MEMBERS:
            assert member in names, f"missing zip member {member}"
        theatre = zf.read("theatre").decode("utf-8")
        assert "Kola" in theatre
        assert "Falklands" not in theatre
        assert "TheChannel" not in theatre
        mission = zf.read("mission").decode("utf-8")
        for token in KOLA_MISSION_CONTRACTS:
            assert token in mission, f"missing mission contract {token}"
        assert '["type"]="Su-25T"' in mission
        assert "Norway" in mission
        assert "ThirdReich" not in mission
        assert "MountPleasant" not in mission
        assert "Nellis" not in mission
