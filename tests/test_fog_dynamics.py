"""Fog dynamics Spec + curated setFogAnimation DoScript emit."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.fog_dynamics import build_fog_animation_lua
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import FogDynamics, FogDynamicsMode
from dcs_miz_planner.tools.surface import validate_mission_spec

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples" / "manston_dawn_fog_burnoff.yaml"


def test_fog_lua_burn_off_template() -> None:
    lua = build_fog_animation_lua(
        FogDynamics(mode=FogDynamicsMode.BURN_OFF, start_after_s=0, duration_s=1200)
    )
    assert "setFogAnimation" in lua
    assert "1200" in lua


def test_fog_lua_roll_in_template() -> None:
    lua = build_fog_animation_lua(
        FogDynamics(
            mode=FogDynamicsMode.ROLL_IN,
            duration_s=900,
            end_visibility_m=2500,
            end_thickness_m=180,
        )
    )
    assert "900" in lua
    assert "2500" in lua
    assert "180" in lua


def test_fog_dynamics_example_validates_and_compiles(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    assert validate_mission_spec(EXAMPLE, inventory=inv)["ok"]
    miz = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(EXAMPLE), tmp_path / "fog.miz", voice="raf"
    )
    with zipfile.ZipFile(miz) as z:
        mission = z.read("mission").decode("utf-8")
        # Script body lives in dictionary / mission strings.
        blob = mission
        for name in z.namelist():
            if "l10n" in name or name.endswith(".lua"):
                blob += z.read(name).decode("utf-8", errors="ignore")
        # Dict keys may hold the script; scan whole zip textually.
        texts = []
        for name in z.namelist():
            raw = z.read(name)
            try:
                texts.append(raw.decode("utf-8"))
            except UnicodeDecodeError:
                continue
        joined = "\n".join(texts)
    assert "setFogAnimation" in joined
    assert "1200" in joined
