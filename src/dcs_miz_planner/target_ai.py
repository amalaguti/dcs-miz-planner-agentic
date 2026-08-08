"""Resolve and emit curated ground/sea target WP AI options (#15h / R12)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .models import (
    GroundTarget,
    TargetAi,
    TargetAlarmState,
    TargetMoveFormation,
    TargetRestrictTargets,
    TargetRoe,
)

TargetAiClass = Literal["soft", "aaa", "sea"]

# Channel registry AAA / AT / searchlight / director ids (strike_target_class aaa_guns).
_AAA_UNIT_IDS = frozenset(
    {
        "flak18",
        "flak30",
        "flak36",
        "flak37",
        "flak38",
        "flak41",
        "Flakscheinwerfer_37",
        "KDO_Mod40",
        "Allies_Director",
        "M45_Quadmount",
        "QF_37_AA",
        "Pak40",
        "bofors40",
    }
)

_SOFT_AI_KEYS = frozenset({"roe", "alarm_state", "engage_air_weapons", "restrict_targets"})
_AAA_AI_KEYS = _SOFT_AI_KEYS | {"interception_range"}
_SEA_AI_KEYS = frozenset({"roe", "alarm_state", "engage_air_weapons", "interception_range"})

_ALARM_VALUES = {
    TargetAlarmState.AUTO: 0,
    TargetAlarmState.GREEN: 1,
    TargetAlarmState.RED: 2,
}


@dataclass(frozen=True)
class ResolvedTargetAi:
    """Merged preset + explicit AI / move_formation for emit."""

    roe: TargetRoe | None = None
    alarm_state: TargetAlarmState | None = None
    engage_air_weapons: bool | None = None
    restrict_targets: TargetRestrictTargets | None = None
    interception_range: int | None = None
    move_formation: TargetMoveFormation | None = None

    def has_emit(self) -> bool:
        return any(
            v is not None
            for v in (
                self.roe,
                self.alarm_state,
                self.engage_air_weapons,
                self.restrict_targets,
                self.interception_range,
                self.move_formation,
            )
        )


def target_ai_class(unit_id: str, *, domain: str) -> TargetAiClass:
    if domain == "sea":
        return "sea"
    if unit_id in _AAA_UNIT_IDS:
        return "aaa"
    return "soft"


def allowed_ai_keys(ai_class: TargetAiClass) -> frozenset[str]:
    if ai_class == "sea":
        return _SEA_AI_KEYS
    if ai_class == "aaa":
        return _AAA_AI_KEYS
    return _SOFT_AI_KEYS


def _preset_defaults(preset: str) -> tuple[TargetAi, TargetMoveFormation | None]:
    if preset == "convoy_transit":
        return (
            TargetAi(
                roe=TargetRoe.RETURN_FIRE,
                alarm_state=TargetAlarmState.GREEN,
                engage_air_weapons=False,
            ),
            TargetMoveFormation.OFF_ROAD,
        )
    if preset == "aaa_alert":
        return (
            TargetAi(
                roe=TargetRoe.OPEN_FIRE,
                alarm_state=TargetAlarmState.RED,
                engage_air_weapons=True,
                interception_range=100,
            ),
            None,
        )
    if preset == "ship_under_way":
        return (
            TargetAi(
                roe=TargetRoe.RETURN_FIRE,
                alarm_state=TargetAlarmState.GREEN,
            ),
            None,
        )
    if preset == "harbour_static":
        return (
            TargetAi(
                roe=TargetRoe.WEAPONS_HOLD,
                alarm_state=TargetAlarmState.AUTO,
            ),
            None,
        )
    raise ValueError(f"unknown ai_preset {preset!r}")


def resolve_target_ai(tgt: GroundTarget) -> ResolvedTargetAi:
    """Expand preset then overlay explicit ``ai`` / ``move_formation``."""
    base = TargetAi()
    move: TargetMoveFormation | None = None
    if tgt.ai_preset:
        base, move = _preset_defaults(tgt.ai_preset)
    if tgt.ai is not None:
        data = base.model_dump()
        overlay = tgt.ai.model_dump(exclude_none=True)
        data.update(overlay)
        base = TargetAi.model_validate(data)
    if tgt.move_formation is not None:
        move = tgt.move_formation
    return ResolvedTargetAi(
        roe=base.roe,
        alarm_state=base.alarm_state,
        engage_air_weapons=base.engage_air_weapons,
        restrict_targets=base.restrict_targets,
        interception_range=base.interception_range,
        move_formation=move,
    )


def point_action_for_formation(formation: TargetMoveFormation):
    from dcs.point import PointAction

    return {
        TargetMoveFormation.OFF_ROAD: PointAction.OffRoad,
        TargetMoveFormation.ON_ROAD: PointAction.OnRoad,
        TargetMoveFormation.RANK: PointAction.LineAbreast,
        TargetMoveFormation.CONE: PointAction.Cone,
        TargetMoveFormation.VEE: PointAction.Vee,
        TargetMoveFormation.DIAMOND: PointAction.Diamond,
        TargetMoveFormation.ECHELON_LEFT: PointAction.EchelonLeft,
        TargetMoveFormation.ECHELON_RIGHT: PointAction.EchelonRight,
    }[formation]


def apply_move_formation(group: Any, formation: TargetMoveFormation, *, domain: str) -> None:
    """Set PointAction on all land route points."""
    if domain != "land" or not group.points:
        return
    action = point_action_for_formation(formation)
    for pt in group.points:
        pt.action = action


def apply_target_ai_options(group: Any, resolved: ResolvedTargetAi, *, domain: str) -> None:
    """Attach Opt* on WP0 and land PointAction when resolved."""
    from dcs.task import (
        OptAlarmState,
        OptEngageAirWeapons,
        OptInterceptionRange,
        OptRestrictTargets,
        OptROE,
    )

    if not group.points:
        return
    wp0 = group.points[0]
    if resolved.roe is not None:
        roe_map = {
            TargetRoe.OPEN_FIRE: OptROE.Values.OpenFire,
            TargetRoe.RETURN_FIRE: OptROE.Values.ReturnFire,
            TargetRoe.WEAPONS_HOLD: OptROE.Values.WeaponHold,
        }
        wp0.add_task(OptROE(roe_map[resolved.roe]))
    if resolved.alarm_state is not None:
        wp0.add_task(OptAlarmState(_ALARM_VALUES[resolved.alarm_state]))
    if resolved.engage_air_weapons is not None:
        wp0.add_task(OptEngageAirWeapons(bool(resolved.engage_air_weapons)))
    if resolved.restrict_targets is not None and domain == "land":
        rt_map = {
            TargetRestrictTargets.ALL: OptRestrictTargets.Values.AllUnits,
            TargetRestrictTargets.AIR_ONLY: OptRestrictTargets.Values.AirUnitsOnly,
            TargetRestrictTargets.GROUND_ONLY: OptRestrictTargets.Values.GroundUnitsOnly,
        }
        wp0.add_task(OptRestrictTargets(rt_map[resolved.restrict_targets]))
    if resolved.interception_range is not None:
        wp0.add_task(OptInterceptionRange(int(resolved.interception_range)))
    if resolved.move_formation is not None:
        apply_move_formation(group, resolved.move_formation, domain=domain)
