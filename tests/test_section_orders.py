"""Player flight section orders (F10 + AITaskPush)."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory
from pydantic import ValidationError

from dcs_miz_planner.agent.voice import build_commander_brief
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import (
    MissionDate,
    MissionSpec,
    MissionType,
    Player,
    PlayerFlight,
    PlayerFlightRole,
    SectionOrder,
    WeatherPreset,
)
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples" / "manston_cap_flight_orders.yaml"
BASE_WINGMAN = REPO / "examples" / "manston_cap_flight_wingman.yaml"


def test_unknown_order_rejected_at_load() -> None:
    with pytest.raises(ValidationError):
        PlayerFlight(size=2, role=PlayerFlightRole.WINGMAN, orders=["not_a_real_order"])  # type: ignore[list-item]


def test_duplicate_order_rejected() -> None:
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
                orders=[SectionOrder.REJOIN, SectionOrder.REJOIN],
            ),
        ),
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "duplicate_section_order" for e in result.errors)


def test_orders_example_validates_and_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(EXAMPLE)
    assert validate_mission_spec(spec, inventory=inv).ok
    miz = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "orders.miz", voice="raf")
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
        dictionary = z.read("l10n/DEFAULT/dictionary").decode("utf-8")
    assert "a_ai_task" in mission or "AITask" in mission or "ai_task" in mission
    assert "Section: Rejoin" in dictionary or "rejoin" in dictionary.lower()
    assert "section_orders_menu" in mission
    assert "a_add_radio_item" in mission or "AddRadioItem" in mission or "radio" in mission.lower()


def test_omit_orders_no_section_menu(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(BASE_WINGMAN), tmp_path / "plain.miz", voice="raf"
    )
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
    assert "section_orders_menu" not in mission


def test_brief_mentions_orders() -> None:
    brief = build_commander_brief(load_mission_spec(EXAMPLE), "raf")
    assert "section order" in brief.lower() or "f10" in brief.lower()
    plain = build_commander_brief(load_mission_spec(BASE_WINGMAN), "raf")
    assert "rejoin, engage" not in plain.lower()
