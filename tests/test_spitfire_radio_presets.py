"""Channel Spitfire A–E radio bank on compiled .miz (stock Instant Action copy)."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import channel_available_inventory, compile_manston

from dcs_miz_planner.compiler.pydcs_compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec

_CHANNEL_BANK = (124.0, 40.0, 41.0, 42.0, 108.9)
_REPO = Path(__file__).resolve().parents[1]


def _player_group(miz_path: Path, country_name: str):
    from dcs.mission import Mission
    from dcs.unit import Skill

    loaded = Mission()
    loaded.load_file(str(miz_path))
    country = loaded.country(country_name)
    assert country is not None
    for group in country.plane_group:
        for unit in group.units:
            if unit.skill == Skill.Player:
                return group, unit
    raise AssertionError(f"no Player unit in {country_name}")


def test_manston_spitfire_emits_channel_ae_bank(tmp_path: Path) -> None:
    miz = compile_manston(tmp_path / "manston.miz")
    group, unit = _player_group(miz, "UK")
    assert group.radio_set is False
    assert float(group.frequency) == 124.0
    assert unit.radio is not None
    channels = unit.radio[1]["channels"]
    assert tuple(float(channels[i]) for i in range(1, 6)) == _CHANNEL_BANK


def test_p51_does_not_get_spitfire_channel_bank(tmp_path: Path) -> None:
    spec = load_mission_spec(_REPO / "examples" / "manston_p51_freeflight.yaml")
    miz = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "p51.miz", voice="raf"
    )
    _group, unit = _player_group(miz, "USA")
    radio = unit.radio
    if radio is None:
        return
    channels = radio[1]["channels"]
    bank = tuple(float(channels[i]) for i in range(1, 6))
    assert bank != _CHANNEL_BANK
