"""Opt-in dynamics expand pack → typed triggers (Layer B play-time variation)."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.dynamics import DynamicsError, apply_dynamics, expand_dynamics_if_needed
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import DynamicsMode
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "examples" / "manston_dawn_intercept_dynamics_live.yaml"
HYBRID = ROOT / "examples" / "manston_dawn_intercept_dynamics_hybrid.yaml"
RADIO = ROOT / "examples" / "manston_dawn_intercept_radio.yaml"
INTERCEPT_NARRATIVE = ROOT / "examples" / "manston_dawn_intercept_narrative.yaml"


def test_live_example_loads_with_dynamics():
    spec = load_mission_spec(LIVE)
    assert spec.dynamics is not None
    assert spec.dynamics.mode.value == "live"
    assert len(spec.dynamics.pools) == 3
    assert spec.triggers == []


def test_expand_live_emits_roll_and_activates():
    spec = load_mission_spec(LIVE)
    expanded = apply_dynamics(spec)
    assert expanded.dynamics is None
    names = [t.name for t in expanded.triggers]
    assert names[0] == "dynamics_roll"
    assert names[1:] == [
        "dynamics_activate_easy",
        "dynamics_activate_medium",
        "dynamics_activate_hard",
    ]
    roll = expanded.triggers[0].then[0]
    assert roll.type == "set_flag_random"
    assert roll.flag == "raid_die"
    assert roll.min == 1 and roll.max == 3
    assert expanded.triggers[1].then[0].type == "activate_group"
    assert expanded.triggers[1].then[0].enemy_index == 0


def test_expand_hybrid_emits_menu_auto_and_roll_paths():
    spec = load_mission_spec(HYBRID)
    expanded = apply_dynamics(spec)
    assert expanded.dynamics is None
    names = [t.name for t in expanded.triggers]
    assert names[0] == "dynamics_radio_menu"
    assert names[1] == "dynamics_auto_roll"
    assert "dynamics_menu_easy" in names
    assert "dynamics_roll_easy" in names
    radio = expanded.triggers[0].then
    assert radio[0].type == "radio_item_add"
    assert radio[0].label == "Auto (random)"
    assert len(radio) == 4  # Auto + 3 difficulties


def test_conflict_with_hand_triggers():
    spec = load_mission_spec(RADIO)
    base = load_mission_spec(LIVE)
    conflicted = spec.model_copy(update={"dynamics": base.dynamics})
    with pytest.raises(DynamicsError) as exc:
        apply_dynamics(conflicted)
    assert exc.value.code == "dynamics_conflict"
    result = validate_mission_spec(conflicted)
    assert not result.ok
    assert any(e.code == "dynamics_conflict" for e in result.errors)


def test_xor_with_narrative():
    narr = load_mission_spec(INTERCEPT_NARRATIVE)
    live = load_mission_spec(LIVE)
    both = narr.model_copy(update={"dynamics": live.dynamics})
    with pytest.raises(DynamicsError) as exc:
        apply_dynamics(both)
    assert exc.value.code == "dynamics_narrative_xor"
    result = validate_mission_spec(both)
    assert not result.ok
    assert any(e.code == "dynamics_narrative_xor" for e in result.errors)


def test_missing_late_activation_fails():
    spec = load_mission_spec(LIVE)
    enemies = [e.model_copy(update={"late_activation": False}) for e in spec.enemies]
    bad = spec.model_copy(update={"enemies": enemies})
    with pytest.raises(DynamicsError) as exc:
        apply_dynamics(bad)
    assert exc.value.code == "dynamics_enemy_not_late"


def test_bad_enemy_index_fails():
    spec = load_mission_spec(LIVE)
    pools = list(spec.dynamics.pools)
    pools[0] = pools[0].model_copy(update={"enemy_indices": [99]})
    bad = spec.model_copy(update={"dynamics": spec.dynamics.model_copy(update={"pools": pools})})
    with pytest.raises(DynamicsError) as exc:
        apply_dynamics(bad)
    assert exc.value.code == "dynamics_enemy_index"


def test_fixed_emits_no_triggers():
    spec = load_mission_spec(LIVE)
    fixed = spec.model_copy(
        update={
            "dynamics": spec.dynamics.model_copy(update={"mode": DynamicsMode.FIXED, "pools": []}),
        }
    )
    expanded = apply_dynamics(fixed)
    assert expanded.dynamics is None
    assert expanded.triggers == []


def test_expand_noop_when_absent():
    spec = load_mission_spec(RADIO)
    assert expand_dynamics_if_needed(spec).triggers == spec.triggers


def test_validate_and_compile_live(tmp_path: Path):
    spec = load_mission_spec(LIVE)
    assert validate_mission_spec(spec).ok
    out = PyDCSCompiler().compile(spec, tmp_path / "dyn_live.miz")
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "a_set_flag_random" in mission
    assert "a_activate_group" in mission


def test_validate_and_compile_hybrid(tmp_path: Path):
    spec = load_mission_spec(HYBRID)
    assert validate_mission_spec(spec).ok
    out = PyDCSCompiler().compile(spec, tmp_path / "dyn_hybrid.miz")
    mission = zipfile.ZipFile(out).read("mission").decode("utf-8", "replace")
    assert "a_set_flag_random" in mission
    assert "a_activate_group" in mission
    # Radio items appear as AddRadioItem in ME / PyDCS output
    assert "RadioItem" in mission or "radio" in mission.lower()
