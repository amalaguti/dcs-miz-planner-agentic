"""End-to-end: example spec compiles to a valid .miz with expected content."""

from __future__ import annotations

import zipfile
from datetime import UTC, datetime
from pathlib import Path

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.install.models import AvailabilityState, TheatreInventory, TheatreRecord
from dcs_miz_planner.loader import load_mission_spec

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "manston_cold_freeflight.yaml"
REQUIRED_MEMBERS = {"mission", "options", "theatre", "warehouses"}


def _channel_available() -> TheatreInventory:
    return TheatreInventory(
        scanned_at=datetime.now(UTC),
        dcs_roots=("S:/DCS World",),
        saved_games_roots=(),
        theatres=(
            TheatreRecord(
                theatre_id="TheChannel",
                update_id="THECHANNEL_terrain",
                dcs_root="S:/DCS World",
                state=AvailabilityState.AVAILABLE,
                planner_supported=True,
            ),
        ),
    )


def test_manston_example_compiles(tmp_path):
    spec = load_mission_spec(EXAMPLE)
    out = PyDCSCompiler(inventory=_channel_available()).compile(spec, tmp_path / "manston.miz")

    assert out.exists()
    with zipfile.ZipFile(out) as z:
        members = set(z.namelist())
        assert REQUIRED_MEMBERS <= members
        assert zipfile.ZipFile(out).testzip() is None
        mission = z.read("mission").decode("utf-8", "ignore")
        theatre = z.read("theatre").decode("utf-8", "ignore")

    assert theatre == "TheChannel"
    assert "SpitfireLFMkIX" in mission
    assert '["airdromeId"]=5' in mission
    assert '["start_time"]=32400' in mission
    assert "TakeOffParking" in mission
    assert '"Player"' in mission
    # Spitfire VHF is ~100-156 MHz; PyDCS's 251 default is unusable in DCS.
    assert '["frequency"]=124.0' in mission


def test_manston_miz_roundtrips_through_pydcs(tmp_path):
    """PyDCS must be able to re-load the .miz it wrote (structural sanity)."""
    from dcs.mission import Mission
    from dcs.planes import SpitfireLFMkIX
    from dcs.unit import Skill

    spec = load_mission_spec(EXAMPLE)
    out = PyDCSCompiler(inventory=_channel_available()).compile(
        spec, tmp_path / "manston_roundtrip.miz"
    )

    loaded = Mission()
    status = loaded.load_file(str(out))
    # Status messages are warnings; load raises on hard failures.
    assert isinstance(status, list)

    assert loaded.terrain.name == "TheChannel"
    assert loaded.start_time.hour == 9
    assert loaded.start_time.minute == 0
    assert loaded.start_time.year == 1944
    assert loaded.start_time.month == 6
    assert loaded.start_time.day == 6

    uk = loaded.country("UK")
    assert uk is not None
    planes = list(uk.plane_group)
    assert len(planes) == 1
    unit = planes[0].units[0]
    assert unit.unit_type is SpitfireLFMkIX or unit.type == SpitfireLFMkIX.id
    assert unit.skill == Skill.Player


def test_spec_exposes_start_seconds():
    spec = load_mission_spec(EXAMPLE)
    assert spec.start_seconds == 32400
