"""Re-weather existing .miz (overwrite) — Spec sidecar and miz-patch paths."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.reweather import reweather_mission
from dcs_miz_planner.tools.surface import reweather_mission_file

REPO = Path(__file__).resolve().parents[1]
BROKEN = REPO / "examples" / "manston_broken_channel.yaml"
RAIN = "rain_overcast"


def _mission_snippet(miz: Path) -> str:
    with zipfile.ZipFile(miz) as z:
        return z.read("mission").decode("utf-8")


def test_reweather_spec_sidecar(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(BROKEN)
    miz = tmp_path / "sortie.miz"
    yaml_path = tmp_path / "sortie.yaml"
    shutil.copy(BROKEN, yaml_path)
    PyDCSCompiler(inventory=inv).compile(spec, miz, voice="raf")
    before = _mission_snippet(miz)
    assert "Preset" in before or "preset" in before.lower()

    result = reweather_mission(miz, RAIN, seed=7, spec_path=yaml_path, inventory=inv, voice="raf")
    assert result["ok"]
    assert result["mode"] == "spec_recompile"
    after = _mission_snippet(miz)
    assert "RainyPreset" in after
    updated = load_mission_spec(yaml_path)
    assert updated.weather.value == RAIN
    assert updated.weather_opts is not None
    assert updated.weather_opts.seed == 7


def test_reweather_miz_only_patch(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(BROKEN)
    miz = tmp_path / "only.miz"
    PyDCSCompiler(inventory=inv).compile(spec, miz, voice="raf")
    # No sidecar yaml next to miz
    result = reweather_mission(miz, RAIN, seed=11, inventory=inv)
    assert result["ok"]
    assert result["mode"] == "miz_patch"
    assert "RainyPreset" in _mission_snippet(miz)


def test_reweather_tool_surface(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    spec = load_mission_spec(BROKEN)
    miz = tmp_path / "tool.miz"
    yaml_path = tmp_path / "tool.yaml"
    shutil.copy(BROKEN, yaml_path)
    PyDCSCompiler(inventory=inv).compile(spec, miz, voice="raf")
    out = reweather_mission_file(miz, "broken_channel", seed=3, spec_path=yaml_path)
    assert out["ok"]
    assert out["mode"] == "spec_recompile"
    assert Path(out["miz_path"]).is_file()
