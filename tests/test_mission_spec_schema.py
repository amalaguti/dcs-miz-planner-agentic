"""Mission Spec contract: schema_version, unknown-field rejection, reserved extensions."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from dcs_miz_planner.loader import SpecLoadError, load_mission_spec

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "manston_cold_freeflight.yaml"


def _base_spec() -> dict:
    return yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))


def _write(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    return p


def test_valid_manston_spec_loads(tmp_path):
    spec = load_mission_spec(_write(tmp_path, _base_spec()))
    assert spec.schema_version == "1"
    assert spec.player.aircraft == "SpitfireLFMkIX"
    assert spec.enemies == []
    assert spec.objectives == []
    assert spec.triggers == []


def test_missing_schema_version_rejected(tmp_path):
    data = _base_spec()
    del data["schema_version"]
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "schema_version" in str(exc.value)


def test_unsupported_schema_version_rejected(tmp_path):
    data = _base_spec()
    data["schema_version"] = "2"
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "schema_version" in str(exc.value)


def test_unknown_top_level_key_rejected(tmp_path):
    data = _base_spec()
    data["theatr"] = "TheChannel"  # typo of "theatre"
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "theatr" in str(exc.value)


def test_unknown_nested_key_rejected(tmp_path):
    data = _base_spec()
    data["player"]["airfeld"] = "Manston"  # typo of "airfield"
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "airfeld" in str(exc.value)


def test_non_empty_enemies_rejected(tmp_path):
    data = _base_spec()
    data["enemies"] = [{"aircraft": "Bf-109K-4", "count": 4}]
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "free_flight" in str(exc.value) or "not supported" in str(exc.value)


def test_non_empty_triggers_must_be_typed(tmp_path):
    data = _base_spec()
    data["triggers"] = [{"when": "start", "do": "message"}]
    with pytest.raises(SpecLoadError) as exc:
        load_mission_spec(_write(tmp_path, data))
    assert "triggers" in str(exc.value).lower() or "when" in str(exc.value).lower()


def test_typed_time_message_trigger_loads(tmp_path):
    data = _base_spec()
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 60}],
            "then": [{"type": "message", "text": "Push."}],
        }
    ]
    spec = load_mission_spec(_write(tmp_path, data))
    assert len(spec.triggers) == 1
    assert spec.triggers[0].then[0].type == "message"


def test_intercept_example_loads():
    path = Path(__file__).resolve().parents[1] / "examples" / "manston_dawn_intercept.yaml"
    spec = load_mission_spec(path)
    assert spec.mission_type.value == "intercept"
    assert len(spec.enemies) == 1
    assert spec.enemies[0].aircraft == "Bf-109K-4"
    assert spec.objectives[0].type.value == "intercept_enemy"


def test_non_dict_yaml_rejected(tmp_path):
    p = tmp_path / "spec.yaml"
    p.write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)
