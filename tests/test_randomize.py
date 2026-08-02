"""Seeded Spec→Spec randomization."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from dcs_miz_planner.cli import main
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import MissionSpec, WeatherPreset
from dcs_miz_planner.randomize import (
    AXES,
    RandomizeError,
    axes_that_differ,
    parse_axes,
    randomize_mission_spec,
)
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.tools import randomize_mission
from dcs_miz_planner.validation import validate_mission_spec

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "examples" / "manston_cold_freeflight.yaml"
CAP = ROOT / "examples" / "manston_cap.yaml"


def test_parse_axes_unknown():
    with pytest.raises(RandomizeError, match="Unknown"):
        parse_axes("weather,nope")


def test_parse_axes_default_all():
    assert parse_axes(None) == AXES


def test_same_seed_stable_free_flight():
    base = load_mission_spec(FREE)
    a = randomize_mission_spec(base, 42)
    b = randomize_mission_spec(base, 42)
    assert a == b
    assert a.player == base.player
    assert a.mission_type == base.mission_type
    assert a.theatre == base.theatre


def test_different_seeds_may_differ_cap():
    base = load_mission_spec(CAP)
    a = randomize_mission_spec(base, 1)
    b = randomize_mission_spec(base, 2)
    assert a != b
    assert axes_that_differ(a, b)


def test_weather_axis_only():
    base = load_mission_spec(FREE)
    out = randomize_mission_spec(base, 7, axes=["weather"])
    assert out.start_time == base.start_time
    assert out.player == base.player
    assert out.weather in WeatherPreset


def test_geometry_preserves_engagement():
    base = load_mission_spec(CAP)
    out = randomize_mission_spec(base, 99, axes=["geometry"])
    assert out.cap is not None and base.cap is not None
    assert out.cap.engagement == base.cap.engagement
    assert out.cap.pattern == base.cap.pattern
    assert out.enemies == base.enemies


def test_opposition_keeps_registry_fighters():
    base = load_mission_spec(CAP)
    out = randomize_mission_spec(base, 3, axes=["opposition"])
    known = set(get_channel_registry().list_aircraft())
    for enemy in out.enemies:
        assert enemy.aircraft in known
        assert 1 <= enemy.count <= 16


def test_bad_seed_rejected():
    base = load_mission_spec(FREE)
    with pytest.raises(RandomizeError):
        randomize_mission_spec(base, -1)


def test_tool_randomize_mission_ok():
    result = randomize_mission(seed=42, spec_path=FREE)
    assert result["ok"] is True
    assert result["seed"] == 42
    assert result["spec"]["player"]["airfield"] == "Manston"
    assert validate_mission_spec(MissionSpec.model_validate(result["spec"])).ok


def test_tool_unknown_axis_fails():
    result = randomize_mission(seed=1, spec_path=FREE, axes=["bogus"])
    assert result["ok"] is False


def test_cli_randomize_writes_valid(tmp_path: Path):
    out = tmp_path / "r.yaml"
    code = main(["randomize", str(CAP), "--seed", "5", "-o", str(out)])
    assert code == 0
    assert out.is_file()
    spec = load_mission_spec(out)
    assert validate_mission_spec(spec).ok
    data = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert data["player"]["airfield"] == "Manston"
