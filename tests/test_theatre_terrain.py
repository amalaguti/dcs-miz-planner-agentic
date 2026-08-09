"""Theatre → PyDCS terrain binding."""

from __future__ import annotations

from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.theatre_terrain import (
    TheatreTerrainError,
    bound_theatre_ids,
    terrain_for_theatre,
)
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
MANSTON = REPO / "examples" / "manston_cold_freeflight.yaml"


def test_channel_terrain_binds() -> None:
    terrain = terrain_for_theatre("TheChannel")
    assert terrain.__class__.__name__ == "TheChannel"
    assert "TheChannel" in bound_theatre_ids()


def test_normandy_in_bound_set() -> None:
    assert "Normandy" in bound_theatre_ids()
    assert terrain_for_theatre("Normandy").__class__.__name__ == "Normandy"


def test_unbound_theatre_raises() -> None:
    with pytest.raises(TheatreTerrainError, match="No PyDCS terrain binding"):
        terrain_for_theatre("NotARealTheatre")


def test_registry_theatres_are_bound() -> None:
    registry = get_channel_registry()
    bound = bound_theatre_ids()
    missing = [t for t in registry.list_theatres() if t not in bound]
    assert not missing, f"Registry theatres missing terrain bindings: {missing}"


def test_compile_uses_bound_channel(tmp_path: Path) -> None:
    spec = load_mission_spec(MANSTON)
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(spec, tmp_path / "out.miz")
    assert out.is_file()


def test_compile_unbound_theatre_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner import theatre_terrain as tt

    monkeypatch.setattr(tt, "_TERRAIN_FACTORIES", {})

    spec = load_mission_spec(MANSTON)
    compiler = PyDCSCompiler(inventory=channel_available_inventory())
    monkeypatch.setattr(compiler, "_validate", lambda _spec: None)
    with pytest.raises(ValueError, match="No PyDCS terrain binding"):
        compiler.compile(spec, tmp_path / "bad.miz")


def test_validate_unbound_registry_theatre(monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner import theatre_terrain as tt
    from dcs_miz_planner import validation as val

    monkeypatch.setattr(tt, "_TERRAIN_FACTORIES", {})
    monkeypatch.setattr(val, "bound_theatre_ids", tt.bound_theatre_ids)

    spec = load_mission_spec(MANSTON)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert not result.ok
    assert any(e.code == "theatre_terrain_unbound" for e in result.errors)
