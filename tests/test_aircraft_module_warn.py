"""Hermetic tests for aircraft module soft-warns."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from dcs_miz_planner.install.aircraft_modules import (
    aircraft_module_present,
    missing_aircraft_module_messages,
)
from dcs_miz_planner.install.models import AvailabilityState, TheatreInventory, TheatreRecord
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
MANSTON = REPO / "examples" / "manston_cold_freeflight.yaml"


def _inventory(root: Path) -> TheatreInventory:
    return TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=(str(root),),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="TheChannel",
                update_id="THECHANNEL_terrain",
                dcs_root=str(root),
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )


def test_missing_spitfire_folder_warns(tmp_path: Path) -> None:
    root = tmp_path / "dcs"
    root.mkdir()
    (root / "Mods" / "terrains").mkdir(parents=True)
    spec = load_mission_spec(MANSTON)
    result = validate_mission_spec(spec, inventory=_inventory(root))
    assert result.ok
    codes = [w.code for w in result.warnings]
    assert "aircraft_module_missing" in codes
    assert any(w.path == "player.aircraft" for w in result.warnings)


def test_present_spitfire_folder_no_warn(tmp_path: Path) -> None:
    root = tmp_path / "dcs"
    spit = root / "Mods" / "aircraft" / "SpitfireLFMkIX"
    spit.mkdir(parents=True)
    spec = load_mission_spec(MANSTON)
    result = validate_mission_spec(spec, inventory=_inventory(root))
    assert result.ok
    assert not any(w.code == "aircraft_module_missing" for w in result.warnings)


def test_no_roots_on_disk_skips(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist"
    inv = TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=(str(missing),),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="TheChannel",
                update_id="THECHANNEL_terrain",
                dcs_root=str(missing),
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )
    spec = load_mission_spec(MANSTON)
    result = validate_mission_spec(spec, inventory=inv)
    # Theatre may fail as not available; module check must not add warnings.
    assert not any(w.code == "aircraft_module_missing" for w in result.warnings)


def test_fw190_hyphen_folder_alias(tmp_path: Path) -> None:
    root = tmp_path / "dcs"
    (root / "CoreMods" / "WWII Units" / "FW-190A-8").mkdir(parents=True)
    assert aircraft_module_present(root, "FW-190A8")
    assert missing_aircraft_module_messages(
        load_mission_spec(MANSTON), (str(root),)
    )  # spitfire still missing
