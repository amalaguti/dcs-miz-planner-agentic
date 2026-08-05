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


RADIO = ROOT / "examples" / "manston_dawn_intercept_radio.yaml"


def test_radio_late_activation_example_loads():
    spec = load_mission_spec(RADIO)
    assert len(spec.enemies) == 3
    assert all(e.late_activation for e in spec.enemies)
    assert any(a.type == "radio_item_add" for t in spec.triggers for a in t.then)
    assert any(a.type == "activate_group" for t in spec.triggers for a in t.then)
    assert validate_mission_spec(spec).ok


def test_compile_radio_late_activation(tmp_path: Path):
    spec = load_mission_spec(RADIO)
    out = PyDCSCompiler().compile(spec, tmp_path / "radio.miz")
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "a_add_radio_item_for_coalition" in mission or "a_add_radio_item" in mission
    assert "a_activate_group" in mission
    assert "lateActivation" in mission
    assert "c_flag_is_true" in mission


def test_activate_group_requires_one_index(tmp_path: Path):
    data = yaml.safe_load(RADIO.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "activate_group"}],
        }
    ]
    p = tmp_path / "bad_act.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_activate_enemy_index_out_of_range(tmp_path: Path):
    data = yaml.safe_load(RADIO.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "activate_group", "enemy_index": 99}],
        }
    ]
    p = tmp_path / "bad_idx.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "enemy_index_out_of_range" for e in result.errors)


def test_cli_validate_radio_example_ok():
    assert main(["validate", str(RADIO)]) == 0


def test_schema_notes_mention_radio_or_late():
    from dcs_miz_planner.agent.spec_schema import build_spec_schema

    for mt in ("cap", "intercept"):
        blob = " ".join(build_spec_schema(mt).notes).lower()
        assert "late_activation" in blob or "radio" in blob


SOUND_FLAGS = ROOT / "examples" / "manston_freeflight_sound_flags.yaml"


def test_sound_flags_example_loads():
    from dcs_miz_planner.sounds import list_sound_assets

    spec = load_mission_spec(SOUND_FLAGS)
    assert any(a.type == "sound" for t in spec.triggers for a in t.then)
    assert any(c.type == "flag_more" for t in spec.triggers for c in t.when)
    assert any(c.type == "time_since_flag" for t in spec.triggers for c in t.when)
    assert any(a.type == "inc_flag" for t in spec.triggers for a in t.then)
    assert "beep" in list_sound_assets()
    assert validate_mission_spec(spec).ok


def test_compile_sound_flags(tmp_path: Path):
    spec = load_mission_spec(SOUND_FLAGS)
    out = PyDCSCompiler().compile(spec, tmp_path / "sound_flags.miz")
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8", "replace")
        names = zf.namelist()
    assert "a_out_sound" in mission
    assert "c_flag_more" in mission
    assert "a_inc_flag" in mission
    assert "a_set_flag_value" in mission
    assert "c_time_since_flag" in mission
    assert any("beep" in n.lower() or n.endswith(".wav") for n in names) or any(
        "l10n/" in n and not n.endswith("mapResource") and not n.endswith("dictionary")
        for n in names
    )


def test_unknown_sound_asset_fails(tmp_path: Path):
    data = _base()
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "sound", "asset_id": "not_a_real_asset"}],
        }
    ]
    p = tmp_path / "bad_sound.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "unknown_sound_asset" for e in result.errors)


def test_sound_path_field_rejected(tmp_path: Path):
    data = _base()
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "sound", "asset_id": "beep", "path": "C:/evil.wav"}],
        }
    ]
    p = tmp_path / "path_sound.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_cli_validate_sound_flags_ok():
    assert main(["validate", str(SOUND_FLAGS)]) == 0


def test_schema_notes_mention_sound_and_numeric_flags():
    from dcs_miz_planner.agent.spec_schema import build_spec_schema

    blob = " ".join(build_spec_schema("free_flight").notes).lower()
    assert "sound" in blob and "asset_id" in blob
    assert "flag_more" in blob or "inc_flag" in blob


LIFE_LESS = ROOT / "examples" / "manston_ground_attack_life_less.yaml"


def test_group_life_less_example_loads():
    spec = load_mission_spec(LIFE_LESS)
    assert any(c.type == "group_life_less" for t in spec.triggers for c in t.when)
    cond = next(c for t in spec.triggers for c in t.when if c.type == "group_life_less")
    assert cond.target_index == 0
    assert cond.percent == 50
    assert validate_mission_spec(spec).ok


def test_compile_group_life_less(tmp_path: Path):
    spec = load_mission_spec(LIFE_LESS)
    out = PyDCSCompiler().compile(spec, tmp_path / "life_less.miz")
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8", "replace")
    assert "c_group_life_less" in mission
    assert "a_out_text_delay" in mission or "MessageToAll" in mission or "out_text" in mission


def test_group_life_less_out_of_range_fails(tmp_path: Path):
    data = yaml.safe_load(LIFE_LESS.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "group_life_less", "target_index": 99, "percent": 50}],
            "then": [{"type": "message", "text": "x"}],
        }
    ]
    p = tmp_path / "oor.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "target_index_out_of_range" for e in result.errors)


def test_group_life_less_both_indices_rejected(tmp_path: Path):
    data = yaml.safe_load(LIFE_LESS.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [
                {
                    "type": "group_life_less",
                    "enemy_index": 0,
                    "target_index": 0,
                    "percent": 50,
                }
            ],
            "then": [{"type": "message", "text": "x"}],
        }
    ]
    p = tmp_path / "both.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_group_life_less_invalid_percent_rejected(tmp_path: Path):
    data = yaml.safe_load(LIFE_LESS.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "group_life_less", "target_index": 0, "percent": 0}],
            "then": [{"type": "message", "text": "x"}],
        }
    ]
    p = tmp_path / "pct.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_cli_validate_group_life_less_ok():
    assert main(["validate", str(LIFE_LESS)]) == 0


def test_schema_notes_mention_group_life_less():
    from dcs_miz_planner.agent.spec_schema import build_spec_schema

    blob = " ".join(build_spec_schema("ground_attack").notes).lower()
    assert "group_life_less" in blob


MARKERS = ROOT / "examples" / "manston_ground_attack_markers.yaml"


def test_markers_example_loads():
    spec = load_mission_spec(MARKERS)
    assert any(z.name == "strike_mark" for z in spec.zones)
    acts = [a for t in spec.triggers for a in t.then]
    assert any(a.type == "smoke" for a in acts)
    assert any(a.type == "mark" for a in acts)
    smoke = next(a for a in acts if a.type == "smoke")
    mark = next(a for a in acts if a.type == "mark")
    assert smoke.zone == "strike_mark" and smoke.color.value == "red"
    assert mark.zone == "strike_mark" and "truck" in mark.text.lower()
    assert validate_mission_spec(spec).ok


def test_compile_markers(tmp_path: Path):
    spec = load_mission_spec(MARKERS)
    out = PyDCSCompiler().compile(spec, tmp_path / "markers.miz")
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8", "replace")
    assert "a_mark_to_all" in mission
    assert "a_explosion_marker" in mission
    assert "a_out_text_delay" in mission or "out_text" in mission


def test_mark_unknown_zone_fails(tmp_path: Path):
    data = yaml.safe_load(MARKERS.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "mark", "zone": "missing", "text": "x"}],
        }
    ]
    p = tmp_path / "noz.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "unknown_zone" for e in result.errors)


def test_smoke_invalid_color_rejected(tmp_path: Path):
    data = yaml.safe_load(MARKERS.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "smoke", "zone": "strike_mark", "color": "purple"}],
        }
    ]
    p = tmp_path / "badcolor.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_mark_empty_text_rejected(tmp_path: Path):
    data = yaml.safe_load(MARKERS.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "mark", "zone": "strike_mark", "text": ""}],
        }
    ]
    p = tmp_path / "emptytext.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_cli_validate_markers_ok():
    assert main(["validate", str(MARKERS)]) == 0


def test_schema_notes_mention_mark_and_smoke():
    from dcs_miz_planner.agent.spec_schema import build_spec_schema

    blob = " ".join(build_spec_schema("ground_attack").notes).lower()
    assert "mark" in blob and "smoke" in blob


GATES = ROOT / "examples" / "manston_freeflight_altitude_speed_gates.yaml"


def test_altitude_speed_gates_example_loads():
    spec = load_mission_spec(GATES)
    conds = [c for t in spec.triggers for c in t.when]
    assert any(c.type == "unit_altitude_higher" for c in conds)
    assert any(c.type == "unit_speed_higher" for c in conds)
    alt = next(c for c in conds if c.type == "unit_altitude_higher")
    spd = next(c for c in conds if c.type == "unit_speed_higher")
    assert alt.altitude_m == 300 and alt.agl is True
    assert spd.speed_kmh == 450
    assert all(t.once is False for t in spec.triggers)
    assert validate_mission_spec(spec).ok


def test_compile_altitude_speed_gates(tmp_path: Path):
    spec = load_mission_spec(GATES)
    out = PyDCSCompiler().compile(spec, tmp_path / "gates.miz")
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8", "replace")
    assert "c_unit_altitude_higher_AGL" in mission
    assert "c_unit_speed_higher" in mission
    assert "a_out_text_delay" in mission or "out_text" in mission


def test_altitude_non_positive_rejected(tmp_path: Path):
    data = yaml.safe_load(GATES.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "unit_altitude_higher", "altitude_m": 0}],
            "then": [{"type": "message", "text": "x"}],
        }
    ]
    p = tmp_path / "badalt.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_speed_non_positive_rejected(tmp_path: Path):
    data = yaml.safe_load(GATES.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "when": [{"type": "unit_speed_lower", "speed_kmh": -1}],
            "then": [{"type": "message", "text": "x"}],
        }
    ]
    p = tmp_path / "badspd.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(SpecLoadError):
        load_mission_spec(p)


def test_altitude_msl_emit(tmp_path: Path):
    data = yaml.safe_load(GATES.read_text(encoding="utf-8"))
    data["triggers"] = [
        {
            "name": "msl_gate",
            "once": True,
            "when": [
                {"type": "time_more", "seconds": 1},
                {"type": "unit_altitude_lower", "altitude_m": 500, "agl": False},
            ],
            "then": [{"type": "message", "text": "low MSL"}],
        }
    ]
    p = tmp_path / "msl.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    assert validate_mission_spec(spec).ok
    out = PyDCSCompiler().compile(spec, tmp_path / "msl.miz")
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8", "replace")
    assert "c_unit_altitude_lower" in mission
    assert "c_unit_altitude_lower_AGL" not in mission


def test_cli_validate_gates_ok():
    assert main(["validate", str(GATES)]) == 0


def test_schema_notes_mention_altitude_and_speed_gates():
    from dcs_miz_planner.agent.spec_schema import build_spec_schema

    blob = " ".join(build_spec_schema("free_flight").notes).lower()
    assert "unit_altitude_higher" in blob and "unit_speed_higher" in blob
    assert "speed_kmh" in blob
