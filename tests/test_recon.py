"""Recon mission type: Spec, validation, and compile."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory, normalize_mission

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import MissionSpec
from dcs_miz_planner.recon import RECON_AOI_ZONE
from dcs_miz_planner.validation import validate_mission_spec

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = REPO_ROOT / "examples" / "manston_recon.yaml"


def _recon_dict(**overrides: object) -> dict:
    data: dict = {
        "schema_version": "1",
        "mission_type": "recon",
        "theatre": "TheChannel",
        "name": "Test Recon",
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
        "recon": {
            "bearing_deg": 125,
            "distance_km": 76,
            "altitude_m": 2000,
            "radius_m": 3000,
            "mark": True,
        },
        "enemies": [],
        "targets": [
            {
                "unit": "Blitz_36-6700A",
                "count": 2,
                "skill": "Average",
                "country": "ThirdReich",
                "coalition": "red",
            }
        ],
        "objectives": [{"type": "recon_area"}],
        "triggers": [],
        "zones": [],
    }
    data.update(overrides)
    return data


def test_example_loads_and_validates() -> None:
    spec = load_mission_spec(EXAMPLE)
    assert spec.mission_type.value == "recon"
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_empty_targets_area_recon() -> None:
    data = _recon_dict(targets=[])
    spec = MissionSpec.model_validate(data)
    result = validate_mission_spec(spec, inventory=channel_available_inventory())
    assert result.ok, result.errors


def test_same_coalition_contact_rejected() -> None:
    data = _recon_dict()
    data["targets"] = [
        {
            "unit": "Blitz_36-6700A",
            "count": 1,
            "skill": "Average",
            "country": "UK",
            "coalition": "blue",
        }
    ]
    with pytest.raises(Exception, match="coalition"):
        MissionSpec.model_validate(data)


def test_payload_refused() -> None:
    data = _recon_dict()
    data["player"] = {**data["player"], "payload": "spitfire_2x250_slipper"}
    with pytest.raises(Exception, match="payload"):
        MissionSpec.model_validate(data)


def test_free_flight_plus_recon_refused() -> None:
    data = _recon_dict(mission_type="free_flight", objectives=[], targets=[], enemies=[])
    with pytest.raises(Exception, match="recon"):
        MissionSpec.model_validate(data)


def test_attack_ground_objective_refused() -> None:
    data = _recon_dict(objectives=[{"type": "attack_ground"}])
    with pytest.raises(Exception, match="recon_area|Unsupported objective"):
        MissionSpec.model_validate(data)


def test_compile_recon_structure(tmp_path: Path) -> None:
    spec = load_mission_spec(EXAMPLE)
    out = tmp_path / "recon.miz"
    PyDCSCompiler(inventory=channel_available_inventory()).compile(spec, out, voice="raf")
    with zipfile.ZipFile(out) as z:
        mission = normalize_mission(z.read("mission").decode("utf-8"))
    assert '["task"]="Reconnaissance"' in mission or "Reconnaissance" in mission
    assert RECON_AOI_ZONE in mission or "recon_aoi" in mission
    assert "Blitz_36-6700A" in mission
    assert "Bombing" not in mission
    assert "British_GP_250LBS_Bomb" not in mission
    assert "recon_area_observed" in mission
    assert "a_out_text_delay" in mission
