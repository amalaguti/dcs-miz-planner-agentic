"""Player flight (multi-ship section) Spec + compile structural asserts."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory

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
    WeatherPreset,
    player_ai_lead_group_size,
    player_flight_is_wingman,
    player_flight_join_up_enabled,
    player_group_size,
    player_human_unit_index,
)
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
LEAD_EXAMPLE = REPO / "examples" / "manston_freeflight_flight_lead.yaml"
WINGMAN_EXAMPLE = REPO / "examples" / "manston_freeflight_flight_wingman.yaml"
CAP_WINGMAN_EXAMPLE = REPO / "examples" / "manston_cap_flight_wingman.yaml"


def _base_player(**overrides) -> Player:
    data = {
        "aircraft": "SpitfireLFMkIX",
        "airfield": "Manston",
        "skill": "Player",
    }
    data.update(overrides)
    return Player(**data)


def _free_flight(player: Player) -> MissionSpec:
    return MissionSpec(
        schema_version="1",
        mission_type=MissionType.FREE_FLIGHT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=player,
    )


def test_helpers_lead_and_wingman_indexes() -> None:
    lead = PlayerFlight(size=4, role=PlayerFlightRole.LEAD)
    wing = PlayerFlight(size=2, role=PlayerFlightRole.WINGMAN)
    assert player_group_size(None) == 1
    assert player_human_unit_index(None) == 0
    assert player_group_size(lead) == 4
    assert player_human_unit_index(lead) == 0
    assert player_group_size(wing) == 1
    assert player_ai_lead_group_size(wing) == 1
    assert player_human_unit_index(wing) == 0
    assert player_flight_is_wingman(wing)
    assert not player_flight_is_wingman(lead)
    assert wing.join_up is True
    assert player_flight_join_up_enabled(wing)
    assert not player_flight_join_up_enabled(lead)
    assert not player_flight_join_up_enabled(
        PlayerFlight(size=2, role=PlayerFlightRole.WINGMAN, join_up=False)
    )


def test_join_up_default_and_opt_out_load() -> None:
    assert PlayerFlight(size=2, role=PlayerFlightRole.WINGMAN).join_up is True
    opt_out = PlayerFlight(size=2, role=PlayerFlightRole.WINGMAN, join_up=False)
    assert opt_out.join_up is False


def test_lead_with_join_up_validates() -> None:
    inv = channel_available_inventory()
    spec = _free_flight(
        _base_player(flight=PlayerFlight(size=2, role=PlayerFlightRole.LEAD, join_up=True))
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert result.ok, result.errors


def test_flight_lead_example_validates() -> None:
    inv = channel_available_inventory()
    result = validate_mission_spec(load_mission_spec(LEAD_EXAMPLE), inventory=inv)
    assert result.ok, result.errors


def test_flight_wingman_example_validates() -> None:
    inv = channel_available_inventory()
    result = validate_mission_spec(load_mission_spec(WINGMAN_EXAMPLE), inventory=inv)
    assert result.ok, result.errors


def test_reject_client_skill_with_flight() -> None:
    inv = channel_available_inventory()
    spec = _free_flight(
        _base_player(
            skill="Client",
            flight=PlayerFlight(size=2, role=PlayerFlightRole.LEAD),
        )
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "player_flight_skill" for e in result.errors)


def test_reject_player_as_ai_skill() -> None:
    inv = channel_available_inventory()
    spec = _free_flight(_base_player(flight=PlayerFlight(size=2, ai_skill="Player")))
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "player_flight_ai_skill" for e in result.errors)


def test_reject_size_one_at_load() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        PlayerFlight(size=1, role=PlayerFlightRole.LEAD)


def _mission_text(miz: Path) -> str:
    with zipfile.ZipFile(miz) as z:
        return z.read("mission").decode("utf-8")


def _player_group_unit_skills(mission: str) -> list[str]:
    """Collect skill strings from the first SpitfireLFMkIX group units block."""
    # Match unit skill entries near SpitfireLFMkIX placements.
    skills = re.findall(
        r'\["skill"\]\s*=\s*"([^"]+)"',
        mission,
    )
    # First group is player; for free-flight lead example expect 4 skills then done.
    return skills


def test_compile_four_ship_lead(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(LEAD_EXAMPLE), tmp_path / "lead.miz", voice="raf"
    )
    text = _mission_text(miz)
    assert text.count("SpitfireLFMkIX") >= 4
    skills = _player_group_unit_skills(text)
    assert skills.count("Player") == 1
    assert skills[0] == "Player"
    assert skills[1:4] == ["Average", "Average", "Average"]


def test_compile_wingman_pair(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(WINGMAN_EXAMPLE), tmp_path / "wing.miz", voice="raf"
    )
    text = _mission_text(miz)
    # Separate AI lead group (size−1) + Player group: Player on its only unit.
    assert "Lead" in text
    assert text.count("SpitfireLFMkIX") >= 4
    skills = _player_group_unit_skills(text)
    assert skills.count("Player") == 1
    assert skills.count("Average") >= 3
    assert skills[:4] == ["Average", "Average", "Average", "Player"]
    assert "Follow" in text or "follow" in text.lower()
    assert "groupId" in text or "groupid" in text.lower()
    assert "Section outbound" in text or "Join" in text


def test_compile_wingman_join_up_opt_out_no_follow(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = _free_flight(
        _base_player(
            flight=PlayerFlight(
                size=2, role=PlayerFlightRole.WINGMAN, join_up=False, ai_skill="Average"
            )
        )
    )
    miz = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "nojoin.miz", voice="raf")
    text = _mission_text(miz)
    assert "Lead" in text
    assert "Follow" not in text


def test_compile_cap_wingman_follow_and_cap_on_lead(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    assert validate_mission_spec(load_mission_spec(CAP_WINGMAN_EXAMPLE), inventory=inv).ok
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(CAP_WINGMAN_EXAMPLE), tmp_path / "cap_wing.miz", voice="raf"
    )
    text = _mission_text(miz)
    assert "Follow" in text or "follow" in text.lower()
    assert '["task"]="CAP"' in text or "CAP" in text
    assert "Orbit" in text or "orbit" in text.lower()


def test_brief_mentions_four_ship_lead() -> None:
    brief = build_commander_brief(load_mission_spec(LEAD_EXAMPLE), "raf")
    assert "section of 4" in brief
    assert "flight lead" in brief


def test_brief_mentions_wingman() -> None:
    brief = build_commander_brief(load_mission_spec(WINGMAN_EXAMPLE), "raf")
    assert "section of 4" in brief
    assert "wingman" in brief
    assert "Follow" in brief or "join up" in brief.lower()
