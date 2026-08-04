"""Opt-in CAP / intercept narrative → typed zones/triggers."""

from __future__ import annotations

import zipfile
from pathlib import Path

import yaml

from dcs_miz_planner.agent.spec_schema import build_spec_schema
from dcs_miz_planner.cli import main
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.narrative import apply_narrative, expand_narrative_if_needed
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "examples" / "manston_cap.yaml"
CAP_NARRATIVE = ROOT / "examples" / "manston_cap_narrative.yaml"
INTERCEPT_NARRATIVE = ROOT / "examples" / "manston_dawn_intercept_narrative.yaml"
FREE = ROOT / "examples" / "manston_cold_freeflight.yaml"


def test_narrative_example_loads_enabled():
    spec = load_mission_spec(CAP_NARRATIVE)
    assert spec.narrative is not None
    assert spec.narrative.enabled
    assert spec.zones == []
    assert spec.triggers == []


def test_expand_cap_narrative_adds_rules():
    spec = load_mission_spec(CAP_NARRATIVE)
    expanded = apply_narrative(spec, voice="raf")
    assert expanded.narrative is not None
    assert expanded.narrative.enabled is False
    assert len(expanded.zones) == 1
    assert expanded.zones[0].name == "cap_station"
    assert len(expanded.triggers) == 3
    names = [t.name for t in expanded.triggers]
    assert names == [
        "narrative_push",
        "narrative_on_station",
        "narrative_bandits_down",
    ]
    assert "Ops — scramble" in expanded.triggers[0].then[0].text
    assert expanded.triggers[2].then[-1].type == "mission_end"


def test_expand_intercept_narrative_adds_rules():
    spec = load_mission_spec(INTERCEPT_NARRATIVE)
    expanded = apply_narrative(spec, voice="raf")
    assert expanded.narrative is not None
    assert expanded.narrative.enabled is False
    assert expanded.zones == []
    assert len(expanded.triggers) == 2
    names = [t.name for t in expanded.triggers]
    assert names == ["narrative_scramble", "narrative_bandits_down"]
    assert "scramble" in expanded.triggers[0].then[0].text.lower()
    assert expanded.triggers[1].then[-1].type == "mission_end"


def test_validate_and_compile_narrative_cap(tmp_path: Path):
    spec = load_mission_spec(CAP_NARRATIVE)
    assert validate_mission_spec(spec, voice="raf").ok
    out = PyDCSCompiler().compile(spec, tmp_path / "cap_narr.miz", voice="raf")
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "c_time_after" in mission
    assert "a_out_text_delay" in mission
    assert "c_group_dead" in mission
    assert "a_end_mission" in mission


def test_validate_and_compile_narrative_intercept(tmp_path: Path):
    spec = load_mission_spec(INTERCEPT_NARRATIVE)
    assert validate_mission_spec(spec, voice="raf").ok
    out = PyDCSCompiler().compile(spec, tmp_path / "int_narr.miz", voice="raf")
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "c_time_after" in mission
    assert "a_out_text_delay" in mission
    assert "c_group_dead" in mission
    assert "a_end_mission" in mission


def test_conflict_with_hand_triggers(tmp_path: Path):
    data = yaml.safe_load(CAP.read_text(encoding="utf-8"))
    data["narrative"] = {"enabled": True}
    data["triggers"] = [
        {
            "when": [{"type": "time_more", "seconds": 1}],
            "then": [{"type": "message", "text": "Hand"}],
        }
    ]
    p = tmp_path / "conflict.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "narrative_conflict" for e in result.errors)


def test_unsupported_mission_type_narrative_rejected(tmp_path: Path):
    data = yaml.safe_load(FREE.read_text(encoding="utf-8"))
    data["narrative"] = {"enabled": True}
    p = tmp_path / "ff.yaml"
    p.write_text(yaml.safe_dump(data), encoding="utf-8")
    spec = load_mission_spec(p)
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "narrative_unsupported_mission_type" for e in result.errors)


def test_intercept_narrative_requires_enemies():
    from dcs_miz_planner.models import NarrativeSpec

    spec = load_mission_spec(INTERCEPT_NARRATIVE).model_copy(
        update={"enemies": [], "narrative": NarrativeSpec(enabled=True)}
    )
    result = validate_mission_spec(spec)
    assert not result.ok
    assert any(e.code == "narrative_enemies_required" for e in result.errors)


def test_disabled_narrative_noop():
    spec = load_mission_spec(CAP)
    assert expand_narrative_if_needed(spec).triggers == []
    assert validate_mission_spec(spec).ok


def test_cli_validate_narrative_ok():
    assert main(["validate", str(CAP_NARRATIVE)]) == 0
    assert main(["validate", str(INTERCEPT_NARRATIVE)]) == 0


def test_schema_notes_mention_narrative():
    for mt in ("cap", "intercept"):
        view = build_spec_schema(mt)
        blob = " ".join(view.notes).lower()
        assert "narrative" in blob
