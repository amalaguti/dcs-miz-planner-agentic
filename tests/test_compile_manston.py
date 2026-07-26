"""PyDCS round-trip smoke for Manston (structural goldens live in test_manston_golden)."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import EXAMPLE_SPEC, compile_manston

from dcs_miz_planner.loader import load_mission_spec


def test_manston_miz_roundtrips_through_pydcs(tmp_path: Path):
    """PyDCS must be able to re-load the .miz it wrote (structural sanity)."""
    from dcs.mission import Mission
    from dcs.planes import SpitfireLFMkIX
    from dcs.unit import Skill

    out = compile_manston(tmp_path / "manston_roundtrip.miz")

    loaded = Mission()
    status = loaded.load_file(str(out))
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
    spec = load_mission_spec(EXAMPLE_SPEC)
    assert spec.start_seconds == 32400
