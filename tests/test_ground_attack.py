"""Ground-attack Mission Spec load/validate and compile smoke tests."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
import yaml
from fixtures_support import channel_available_inventory

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import SpecLoadError, load_mission_spec
from dcs_miz_planner.models import (
    Coalition,
    GroundTarget,
    MissionDate,
    MissionSpec,
    MissionType,
    Objective,
    ObjectiveType,
    Player,
    Strike,
    WeatherPreset,
)
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.validation import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
GA_EXAMPLE = REPO / "examples" / "manston_ground_attack.yaml"
FREE_FLIGHT = REPO / "examples" / "manston_cold_freeflight.yaml"


def _ga_dict(**overrides) -> dict:
    data = yaml.safe_load(GA_EXAMPLE.read_text(encoding="utf-8"))
    data.update(overrides)
    return data


def _write(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


def test_payload_and_ground_unit_registry() -> None:
    reg = get_channel_registry()
    assert "spitfire_2x250_slipper" in reg.list_payloads()
    slipper = reg.get_payload("spitfire_2x250_slipper")
    assert slipper.aircraft == "SpitfireLFMkIX"
    assert any(p.clsid == "SPITFIRE_45GAL_SLIPPER_TANK" for p in slipper.pylons)
    assert "Blitz_36-6700A" in reg.list_ground_units()
    assert reg.get_ground_unit("flak18").id == "flak18"
    assert reg.get_strike_unit("Blitz_36-6700A").domain == "land"
    assert "Schnellboot_type_S130" in reg.list_ships()
    assert reg.get_strike_unit("Schnellboot_type_S130").domain == "sea"


def test_ground_attack_example_loads() -> None:
    spec = load_mission_spec(GA_EXAMPLE)
    assert spec.mission_type is MissionType.GROUND_ATTACK
    assert spec.strike is not None
    assert spec.player.payload == "spitfire_2x250_slipper"
    assert spec.objectives[0].type is ObjectiveType.ATTACK_GROUND
    assert len(spec.targets) == 1
    assert spec.targets[0].coalition is Coalition.RED
    assert not spec.enemies


def test_free_flight_with_strike_rejected(tmp_path: Path) -> None:
    data = yaml.safe_load(FREE_FLIGHT.read_text(encoding="utf-8"))
    data["strike"] = {"bearing_deg": 90, "distance_km": 10, "altitude_m": 2000}
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "strike" in str(exc.value).lower() or "free_flight" in str(exc.value)


def test_friendly_target_rejected(tmp_path: Path) -> None:
    data = _ga_dict()
    data["targets"][0]["coalition"] = "blue"
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "enemy" in str(exc.value).lower() or "coalition" in str(exc.value).lower()


def test_practice_allows_same_coalition_uk_targets(tmp_path: Path) -> None:
    data = _ga_dict()
    # Short hop inland UK from Manston (not mid-Channel): practice range narrative.
    data["strike"] = {
        "bearing_deg": 270,
        "distance_km": 15,
        "altitude_m": 1500,
        "practice": True,
    }
    data["targets"] = [
        {
            "unit": "Bedford_MWD",
            "count": 2,
            "skill": "Average",
            "country": "UK",
            "coalition": "blue",
        }
    ]
    data["name"] = "Manston bombing practice"
    spec = load_mission_spec(_write(tmp_path, data))
    assert spec.strike is not None and spec.strike.practice is True
    assert all(t.coalition is Coalition.BLUE for t in spec.targets)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "ga_practice.miz"
    )
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert "Bedford_MWD" in mission


def test_air_enemies_forbidden(tmp_path: Path) -> None:
    data = _ga_dict()
    data["enemies"] = [
        {
            "aircraft": "Bf-109K-4",
            "count": 1,
            "skill": "Average",
            "country": "ThirdReich",
            "coalition": "red",
        }
    ]
    with pytest.raises(SpecLoadError):
        load_mission_spec(_write(tmp_path, data))


def test_unknown_payload_fails_validation() -> None:
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.GROUND_ATTACK,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(
            aircraft="SpitfireLFMkIX",
            airfield="Manston",
            payload="no_such_loadout",
        ),
        strike=Strike(bearing_deg=140, distance_km=40, altitude_m=2000),
        targets=[
            GroundTarget(unit="Blitz_36-6700A", count=2, coalition=Coalition.RED),
        ],
        objectives=[Objective(type=ObjectiveType.ATTACK_GROUND)],
    )
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert any(e.code == "unknown_payload" for e in result.errors)


def test_unknown_ground_unit_fails_validation() -> None:
    spec = MissionSpec(
        schema_version="1",
        mission_type=MissionType.GROUND_ATTACK,
        theatre="TheChannel",
        date=MissionDate(year=1944, month=6, day=6),
        start_time="09:00",
        weather=WeatherPreset.SUNNY_CLEAR,
        player=Player(
            aircraft="SpitfireLFMkIX",
            airfield="Manston",
            payload="spitfire_2x250_slipper",
        ),
        strike=Strike(bearing_deg=140, distance_km=40, altitude_m=2000),
        targets=[GroundTarget(unit="NoSuchTruck", count=1, coalition=Coalition.RED)],
        objectives=[Objective(type=ObjectiveType.ATTACK_GROUND)],
    )
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert any(e.code == "unknown_strike_unit" for e in result.errors)


def test_ship_target_compiles_mid_channel(tmp_path: Path) -> None:
    data = _ga_dict()
    # Mid-Channel water: ships only (not land trucks).
    data["strike"] = {"bearing_deg": 140, "distance_km": 40, "altitude_m": 2000}
    data["targets"] = [
        {
            "unit": "Schnellboot_type_S130",
            "count": 2,
            "skill": "Average",
            "country": "ThirdReich",
            "coalition": "red",
        }
    ]
    spec = load_mission_spec(_write(tmp_path, data))
    assert get_channel_registry().get_strike_unit("Schnellboot_type_S130").domain == "sea"
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "ga_ship.miz"
    )
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert "Schnellboot_type_S130" in mission


def test_ground_attack_example_validates() -> None:
    spec = load_mission_spec(GA_EXAMPLE)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_ground_attack_compiles(tmp_path: Path) -> None:
    spec = load_mission_spec(GA_EXAMPLE)
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(spec, tmp_path / "ga.miz")
    with zipfile.ZipFile(out) as z:
        mission = z.read("mission").decode("utf-8")
    assert '["task"]="Ground Attack"' in mission or '["task"]="GroundAttack"' in mission
    assert "British_GP_250LBS_Bomb_MK4_on_LH_Spitfire_Wing_Carrier" in mission
    assert "SPITFIRE_45GAL_SLIPPER_TANK" in mission
    assert "Blitz_36-6700A" in mission
    assert "Bombing" in mission
    assert '["frequency"]=124.0' in mission
