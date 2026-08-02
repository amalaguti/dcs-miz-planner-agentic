"""Escort mission type: Spec, validation, and compile."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory, normalize_mission

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import MissionSpec
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.validation import validate_mission_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = REPO_ROOT / "examples" / "manston_escort.yaml"


def _escort_dict(**overrides: object) -> dict:
    data: dict = {
        "schema_version": "1",
        "mission_type": "escort",
        "theatre": "TheChannel",
        "name": "Test Escort",
        "description": "unit test",
        "date": {"year": 1944, "month": 6, "day": 6},
        "start_time": "09:00",
        "weather": "sunny_clear",
        "player": {
            "aircraft": "SpitfireLFMkIX",
            "airfield": "Manston",
            "coalition": "blue",
            "country": "UK",
            "skill": "Player",
            "start": "cold_parking",
        },
        "escort": {
            "bearing_deg": 120,
            "distance_km": 55,
            "altitude_m": 4000,
            "engagement": "weapons_free",
        },
        "package": [
            {
                "aircraft": "MosquitoFBMkVI",
                "count": 2,
                "skill": "Average",
                "country": "UK",
                "coalition": "blue",
            }
        ],
        "enemies": [],
        "objectives": [{"type": "escort_package"}],
        "triggers": [],
        "targets": [],
    }
    data.update(overrides)
    return data


def test_mosquito_in_registry() -> None:
    ref = get_channel_registry().get_aircraft("MosquitoFBMkVI")
    assert ref.radio_mhz == 124.0


def test_example_loads_and_validates() -> None:
    spec = load_mission_spec(EXAMPLE)
    assert spec.mission_type.value == "escort"
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_hostile_package_rejected() -> None:
    data = _escort_dict()
    data["package"] = [
        {
            "aircraft": "MosquitoFBMkVI",
            "count": 1,
            "skill": "Average",
            "country": "ThirdReich",
            "coalition": "red",
        }
    ]
    with pytest.raises(Exception, match="friendly|coalition|package"):
        MissionSpec.model_validate(data)


def test_unknown_package_aircraft_fails_validation() -> None:
    data = _escort_dict()
    data["package"] = [
        {
            "aircraft": "NotAPlane",
            "count": 1,
            "skill": "Average",
            "country": "UK",
            "coalition": "blue",
        }
    ]
    spec = MissionSpec.model_validate(data)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert not result.ok
    assert any(
        e.code == "unknown_aircraft" and e.path and "package" in e.path for e in result.errors
    )


def test_free_flight_rejects_escort_block() -> None:
    data = _escort_dict(mission_type="free_flight")
    data.pop("escort")
    data.pop("package")
    data["objectives"] = []
    data["enemies"] = []
    # Re-add escort on free_flight
    data["escort"] = {
        "bearing_deg": 120,
        "distance_km": 55,
        "altitude_m": 4000,
        "engagement": "weapons_free",
    }
    with pytest.raises(Exception, match="escort"):
        MissionSpec.model_validate(data)


def test_escort_rejects_strike_and_payload() -> None:
    data = _escort_dict()
    data["player"]["payload"] = "spitfire_2x250"
    with pytest.raises(Exception, match="payload"):
        MissionSpec.model_validate(data)


def test_compile_escort_emits_task_and_package(tmp_path: Path) -> None:
    spec = load_mission_spec(EXAMPLE)
    out = PyDCSCompiler(inventory=channel_available_inventory()).compile(
        spec, tmp_path / "escort.miz"
    )
    assert out.is_file()
    with zipfile.ZipFile(out) as z:
        mission = normalize_mission(z.read("mission").decode("utf-8"))
    assert '["task"]="Escort"' in mission
    assert "Escort" in mission  # EscortTaskAction
    assert "groupId" in mission
    assert "MosquitoFBMkVI" in mission
    assert "Bf-109K-4" in mission
    assert "SpitfireLFMkIX" in mission
    assert '["airdromeId"]=5' in mission
    assert '["frequency"]=124.0' in mission
    assert '["value"]=0' in mission  # OptROE WeaponFree
