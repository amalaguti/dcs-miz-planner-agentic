"""CAP Mission Spec load/validate and compile smoke tests."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
import yaml
from fixtures_support import channel_available_inventory

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import SpecLoadError, load_mission_spec
from dcs_miz_planner.models import (
    Cap,
    CapPattern,
    EnemyFlight,
    Engagement,
    MissionDate,
    MissionSpec,
    MissionType,
    Objective,
    ObjectiveType,
    Player,
    WeatherPreset,
)
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
CAP_EXAMPLE = REPO / "examples" / "manston_cap.yaml"
FREE_FLIGHT = REPO / "examples" / "manston_cold_freeflight.yaml"


def _cap_dict(**overrides) -> dict:
    data = yaml.safe_load(CAP_EXAMPLE.read_text(encoding="utf-8"))
    data.update(overrides)
    return data


def _write(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


def test_cap_example_loads():
    spec = load_mission_spec(CAP_EXAMPLE)
    assert spec.mission_type is MissionType.CAP
    assert spec.cap is not None
    assert spec.cap.bearing_deg == 135
    assert spec.cap.pattern is CapPattern.CIRCLE
    assert spec.cap.engagement is Engagement.WEAPONS_FREE
    assert spec.objectives[0].type is ObjectiveType.PATROL
    assert len(spec.enemies) == 1


def test_pure_patrol_cap_loads(tmp_path: Path):
    data = _cap_dict()
    data["enemies"] = []
    spec = load_mission_spec(_write(tmp_path, data))
    assert spec.enemies == []
    assert spec.cap is not None


def test_free_flight_with_cap_rejected(tmp_path: Path):
    data = yaml.safe_load(FREE_FLIGHT.read_text(encoding="utf-8"))
    data["cap"] = {
        "bearing_deg": 90,
        "distance_km": 10,
        "altitude_m": 3000,
        "pattern": "circle",
        "engagement": "weapons_free",
    }
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "cap" in str(exc.value).lower() or "free_flight" in str(exc.value)


def test_bad_engagement_rejected(tmp_path: Path):
    data = _cap_dict()
    data["cap"]["engagement"] = "shoot_everything"
    with pytest.raises(SpecLoadError):
        load_mission_spec(_write(tmp_path, data))


def test_bad_pattern_rejected(tmp_path: Path):
    data = _cap_dict()
    data["cap"]["pattern"] = "figure_eight"
    with pytest.raises(SpecLoadError):
        load_mission_spec(_write(tmp_path, data))


def test_cap_missing_block_rejected():
    with pytest.raises(ValueError, match="cap"):
        MissionSpec(
            schema_version="1",
            mission_type=MissionType.CAP,
            theatre="TheChannel",
            date=MissionDate(year=1944, month=6, day=6),
            start_time="09:00",
            weather=WeatherPreset.SUNNY_CLEAR,
            player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
            objectives=[Objective(type=ObjectiveType.PATROL)],
        )


def test_cap_example_validates():
    spec = load_mission_spec(CAP_EXAMPLE)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok


def test_cap_unknown_enemy_aircraft():
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.CAP,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
        cap=Cap(
            bearing_deg=135,
            distance_km=25,
            altitude_m=4000,
            pattern=CapPattern.CIRCLE,
            engagement=Engagement.WEAPONS_FREE,
        ),
        enemies=[EnemyFlight(aircraft="NoSuchJet", count=1)],
        objectives=[Objective(type=ObjectiveType.PATROL)],
    )
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert any(
        e.code == "unknown_aircraft" and e.path == "enemies[0].aircraft" for e in result.errors
    )


def test_cap_compiles_with_orbit_and_roe(tmp_path: Path):
    spec = load_mission_spec(CAP_EXAMPLE)
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(spec, tmp_path / "cap.miz")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert '["task"]="CAP"' in mission
    assert "Orbit" in mission
    assert '["pattern"]="Circle"' in mission
    assert "ControlledTask" in mission
    assert "Bf-109K-4" in mission
    assert '["value"]=0' in mission  # weapons_free OptROE


def test_cap_race_track_compiles(tmp_path: Path):
    data = _cap_dict()
    data["cap"]["pattern"] = "race_track"
    data["enemies"] = []
    spec = load_mission_spec(_write(tmp_path, data))
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "cap_rt.miz"
    )
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert "Race-Track" in mission or "Race" in mission
