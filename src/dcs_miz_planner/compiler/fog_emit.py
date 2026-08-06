"""Emit curated fog_dynamics DoScript trigger into a PyDCS mission."""

from __future__ import annotations

from typing import Any

from ..fog_dynamics import build_fog_animation_lua
from ..models import MissionSpec


def apply_fog_dynamics(mission: Any, spec: MissionSpec) -> None:
    """Append ONCE time_more → DoScript for Spec ``fog_dynamics`` if set."""
    fog = spec.fog_dynamics
    if fog is None:
        return

    from dcs import action, condition
    from dcs.triggers import TriggerOnce

    lua = build_fog_animation_lua(fog)
    trig = TriggerOnce(comment="fog_dynamics")
    trig.add_condition(condition.TimeAfter(seconds=int(fog.start_after_s)))
    trig.add_action(action.DoScript(mission.string(lua)))
    mission.triggerrules.triggers.append(trig)
