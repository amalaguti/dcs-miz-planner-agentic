"""Aircraft failures Spec + ME SetFailure emit."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent.voice import build_commander_brief
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.compiler.failures_emit import failure_table_entry
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import (
    FailureEvent,
    MissionDate,
    MissionSpec,
    MissionType,
    Player,
    WeatherPreset,
)
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples" / "manston_freeflight_magneto_failure.yaml"
BASE = REPO / "examples" / "manston_cold_freeflight.yaml"


def test_failure_table_entry_within_min_one() -> None:
    row = failure_table_entry(FailureEvent(id="ENG0_MAGNETO0", start_after_s=120))
    assert row["enable"] is True
    assert row["hh"] == 0
    assert row["mm"] == 2
    assert row["mmint"] == 1
    assert row["prob"] == 100


def test_spitfire_failure_catalog() -> None:
    refs = get_channel_registry().list_failures("SpitfireLFMkIX")
    ids = {r.id for r in refs}
    assert "ENG0_MAGNETO0" in ids
    assert "HYDR_PUMP_FAILURE" in ids
    assert get_channel_registry().is_known_failure("SpitfireLFMkIX", "ENG0_MAGNETO0")
    assert not get_channel_registry().list_failures("MosquitoFBMkVI")


def test_unknown_failure_id_rejected() -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(BASE).model_copy(
        update={"failures": [FailureEvent(id="NOT_A_REAL_FAILURE", start_after_s=60)]}
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "unknown_failure_id" for e in result.errors)


def test_failures_unsupported_aircraft_rejected() -> None:
    inv = channel_available_inventory()
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.FREE_FLIGHT,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="MosquitoFBMkVI", airfield="Manston"),
        failures=[FailureEvent(id="ENG0_MAGNETO0", start_after_s=60)],
    )
    result = validate_mission_spec(spec, inventory=inv)
    assert not result.ok
    assert any(e.code == "failures_unsupported_aircraft" for e in result.errors)


def test_magneto_example_validates_and_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(EXAMPLE)
    assert validate_mission_spec(spec, inventory=inv).ok
    miz = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "magneto.miz", voice="raf")
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
        dictionary = z.read("l10n/DEFAULT/dictionary").decode("utf-8")
    assert "ENG0_MAGNETO0" in mission
    assert '["enable"]=true' in mission.replace(" ", "") or '["enable"] = true' in mission
    assert "a_set_failure" not in mission
    assert "mag 1 fails" in dictionary.lower()
    assert "magneto 2 should already be off" in dictionary.lower()


def test_omit_failures_leaves_empty_failures_table(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(BASE), tmp_path / "plain.miz", voice="raf"
    )
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
    assert "a_set_failure" not in mission
    assert "ENG0_MAGNETO0" not in mission


def test_brief_mentions_failures_when_armed() -> None:
    brief = build_commander_brief(load_mission_spec(EXAMPLE), "raf")
    assert "system failure" in brief.lower() or "system failures" in brief.lower()
    plain = build_commander_brief(load_mission_spec(BASE), "raf")
    assert "system failure" not in plain.lower()
