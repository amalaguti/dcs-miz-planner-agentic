"""Emit curated fog_dynamics script trigger into a PyDCS mission."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from ..fog_dynamics import build_fog_animation_lua
from ..models import MissionSpec


def apply_fog_dynamics(mission: Any, spec: MissionSpec) -> None:
    """Append ONCE time_more → DoScriptFile for Spec ``fog_dynamics`` if set."""
    fog = spec.fog_dynamics
    if fog is None:
        return

    from dcs import action, condition
    from dcs.triggers import TriggerOnce

    lua = build_fog_animation_lua(fog)
    # Prefer DoScriptFile over DoScript(mission.string(...)):
    # - Empty/missing dict lookup makes DCS execute the key name itself
    #   ("DictKey_Translation_N") → '=' expected near '<eof>'.
    # - String(lua) without a dict entry is fragile with multiline keys in
    #   trig.actions (pydcs#179).
    tmp_dir = Path(tempfile.mkdtemp(prefix="dcs_fog_"))
    script_path = tmp_dir / "fog_dynamics.lua"
    script_path.write_text(lua, encoding="utf-8", newline="\n")
    res = mission.map_resource.add_resource_file(str(script_path))

    trig = TriggerOnce(comment="fog_dynamics")
    trig.add_condition(condition.TimeAfter(seconds=int(fog.start_after_s)))
    trig.add_action(action.DoScriptFile(res))
    mission.triggerrules.triggers.append(trig)
