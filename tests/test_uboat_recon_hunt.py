"""Channel surfaced U-boat recon + hunt examples."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import channel_available_inventory, normalize_mission

from dcs_miz_planner.channel_domain import recon_domain_for_spec, strike_domain_for_spec
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.validation import validate_mission_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
RECON_EXAMPLE = REPO_ROOT / "examples" / "manston_uboat_recon.yaml"
HUNT_EXAMPLE = REPO_ROOT / "examples" / "manston_uboat_hunt.yaml"


def test_uboat_in_registry_and_pydcs() -> None:
    from dcs.ships import ship_map

    assert "Uboat_VIIC" in ship_map
    ref = get_channel_registry().get_strike_unit("Uboat_VIIC")
    assert ref.domain == "sea"


def test_mid_channel_geometry_is_sea() -> None:
    recon = load_mission_spec(RECON_EXAMPLE)
    hunt = load_mission_spec(HUNT_EXAMPLE)
    assert recon_domain_for_spec(recon) == "sea"
    assert strike_domain_for_spec(hunt) == "sea"


def test_uboat_recon_validates_and_compiles(tmp_path: Path) -> None:
    spec = load_mission_spec(RECON_EXAMPLE)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "uboat_recon.miz", voice="raf"
    )
    with zipfile.ZipFile(out) as z:
        mission = normalize_mission(z.read("mission").decode("utf-8"))
    assert "Uboat_VIIC" in mission
    assert "Reconnaissance" in mission
    assert "recon_aoi" in mission
    assert "Bombing" not in mission
    assert "British_GP_250LBS_Bomb" not in mission


def test_uboat_hunt_validates_and_compiles(tmp_path: Path) -> None:
    spec = load_mission_spec(HUNT_EXAMPLE)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "uboat_hunt.miz", voice="raf"
    )
    with zipfile.ZipFile(out) as z:
        mission = normalize_mission(z.read("mission").decode("utf-8"))
    assert "Uboat_VIIC" in mission
    assert (
        "Ground Attack" in mission
        or "GroundAttack" in mission
        or '["task"]="Ground Attack"' in mission
    )
    assert "British_GP_250LBS_Bomb" in mission or "SPITFIRE_45GAL_SLIPPER_TANK" in mission
