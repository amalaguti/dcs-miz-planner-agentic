"""Player flight discipline (fail-to-follow moving zone)."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent.voice import build_commander_brief
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import (
    DisciplineHardAction,
    MissionDate,
    MissionSpec,
    MissionType,
    Player,
    PlayerFlight,
    PlayerFlightDiscipline,
    PlayerFlightRole,
    WeatherPreset,
)
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples" / "manston_cap_flight_discipline.yaml"
BASE_WINGMAN = REPO / "examples" / "manston_cap_flight_wingman.yaml"


def test_discipline_on_lead_rejected() -> None:
    inv = channel_available_inventory()
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.FREE_FLIGHT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(
            aircraft="SpitfireLFMkIX",
            airfield="Manston",
            flight=PlayerFlight(
                size=2,
                role=PlayerFlightRole.LEAD,
                discipline=PlayerFlightDiscipline(),
            ),
        ),
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "discipline_requires_wingman_join_up" for e in result.errors)


def test_discipline_hard_before_soft_rejected() -> None:
    inv = channel_available_inventory()
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.FREE_FLIGHT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(
            aircraft="SpitfireLFMkIX",
            airfield="Manston",
            flight=PlayerFlight(
                size=2,
                role=PlayerFlightRole.WINGMAN,
                join_up=True,
                discipline=PlayerFlightDiscipline(
                    soft_after_s=60,
                    hard_after_s=30,
                    hard=DisciplineHardAction.MESSAGE_END,
                ),
            ),
        ),
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "discipline_hard_before_soft" for e in result.errors)


def test_discipline_example_validates_and_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(EXAMPLE)
    assert validate_mission_spec(spec, inventory=inv).ok
    miz = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "discipline.miz", voice="raf")
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
        dictionary = z.read("l10n/DEFAULT/dictionary").decode("utf-8")
    assert "section_discipline_bubble" in mission
    assert "c_unit_out_zone_unit" in mission or "unit_out_zone" in mission
    assert "section_discipline_soft" in mission
    assert "rejoin" in dictionary.lower() or "off station" in dictionary.lower()


def test_omit_discipline_no_pack(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(BASE_WINGMAN), tmp_path / "plain.miz", voice="raf"
    )
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
    assert "section_discipline_soft" not in mission


def test_brief_mentions_discipline() -> None:
    brief = build_commander_brief(load_mission_spec(EXAMPLE), "raf")
    assert "section" in brief.lower() and (
        "bubble" in brief.lower() or "rejoin" in brief.lower() or "leaving" in brief.lower()
    )
    plain = build_commander_brief(load_mission_spec(BASE_WINGMAN), "raf")
    assert "leaving the bubble" not in plain.lower()
