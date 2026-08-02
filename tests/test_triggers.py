"""Typed zones / triggers on Mission Spec + native compile."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
import yaml

from dcs_miz_planner.cli import main
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import SpecLoadError, load_mission_spec
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "examples" / "manston_cold_freeflight.yaml"
SAMPLE = ROOT / "examples" / "manston_freeflight_trigger_sample.yaml"
CAP = ROOT / "examples" / "manston_cap.yaml"


def _base() -> dict:
    return yaml.safe_load(FREE.read_text(encoding="utf-8"))


def test_trigger_sample_loads_and_validates():
    spec = load_mission_spec(SAMPLE)
    assert len(spec.triggers) == 1
    assert spec.triggers[0].when[0].type == "time_more"
    assert validate_mission_spec(spec).ok


def test_malformed_trigger_rejected(tmp_path: Path):
    data = _base()
    data["triggers"] = [{"when": "start", "do": "message"}]
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_script_field_rejected(tmp_path: Path):
    data = _base()
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "message", "text": "Hi", "lua": "print(1)"}],
        }
    ]
    p = tmp_path / "lua.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_missing_zone_ref_fails_validation(tmp_path: Path):
    data = _base()
    data["triggers"] = [
        {
            "when": [{"type": "coalition_in_zone", "zone": "missing", "coalition": "blue"}],
            "then": [{"type": "message", "text": "In zone"}],
        }
    ]
    p = tmp_path / "zone.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "unknown_zone" for e in result.errors)


def test_enemy_index_out_of_range(tmp_path: Path):
    data = yaml.safe_load(CAP.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "unit_dead", "enemy_index": 99}],
            "then": [{"type": "mission_end", "result": "win"}],
        }
    ]
    p = tmp_path / "dead.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "enemy_index_out_of_range" for e in result.errors)


def test_compile_sample_emits_trig_predicates(tmp_path: Path):
    spec = load_mission_spec(SAMPLE)
    out = PyDCSCompiler().compile(spec, tmp_path / "sample.miz")
    assert out.is_file()
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "c_time_after" in mission
    assert "a_out_text_delay" in mission
    assert "Manston Tower" in mission or "DictKey_Translation" in mission
    assert '["airdromeId"]=5' in mission or "airdromeId" in mission


def test_cli_validate_sample_ok():
    assert main(["validate", str(SAMPLE)]) == 0


def test_empty_triggers_still_compile(tmp_path: Path):
    spec = load_mission_spec(FREE)
    out = PyDCSCompiler().compile(spec, tmp_path / "ok.miz")
    assert out.is_file()


def test_zone_and_flag_compile(tmp_path: Path):
    data = _base()
    data["zones"] = [{"name": "near", "bearing_deg": 90, "distance_km": 5, "radius_m": 2000}]
    data["triggers"] = [
        {
            "name": "enter",
            "once": True,
            "when": [{"type": "coalition_in_zone", "zone": "near", "coalition": "blue"}],
            "then": [
                {"type": "set_flag", "flag": "entered", "value": True},
                {"type": "message", "text": "Zone entered.", "duration_s": 5},
            ],
        }
    ]
    p = tmp_path / "zone_ok.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    assert validate_mission_spec(spec).ok
    out = PyDCSCompiler().compile(spec, tmp_path / "zone.miz")
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "c_part_of_coalition_in_zone" in mission
    assert "a_set_flag" in mission
    assert "near" in mission
