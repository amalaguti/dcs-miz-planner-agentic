"""Map Mission Spec zones/triggers to PyDCS native ME trigger tables."""

from __future__ import annotations

from typing import Any

from ..models import (
    ActivateGroupAction,
    CoalitionInZoneCondition,
    DeactivateGroupAction,
    FlagIsCondition,
    MessageAction,
    MissionEndAction,
    MissionEndResult,
    MissionSpec,
    RadioItemAddAction,
    RadioItemRemoveAction,
    SetFlagAction,
    TargetDeadCondition,
    TimeMoreCondition,
    TriggerRule,
    UnitDeadCondition,
    opposing_coalition,
)


def apply_zones_and_triggers(
    mission: Any,
    airport: Any,
    spec: MissionSpec,
    enemy_group_ids: list[int],
    target_group_ids: list[int] | None = None,
) -> None:
    """Emit Spec zones/triggers into ``mission.triggers`` / ``triggerrules``.

    ``enemy_group_ids`` must align with ``spec.enemies`` order (PyDCS group ids).
    ``target_group_ids`` must align with ``spec.targets`` order when present.
    """
    if not spec.zones and not spec.triggers:
        return

    from dcs import action, condition
    from dcs.triggers import TriggerContinious, TriggerOnce

    target_ids = target_group_ids if target_group_ids is not None else []

    zone_ids: dict[str, int] = {}
    for zone in spec.zones:
        pos = airport.position.point_from_heading(zone.bearing_deg, zone.distance_km * 1000.0)
        tz = mission.triggers.add_triggerzone(
            pos,
            radius=zone.radius_m,
            hidden=False,
            name=zone.name,
        )
        zone_ids[zone.name] = tz.id

    flag_ids: dict[str, int] = {}

    def flag_id(name: str) -> int:
        if name not in flag_ids:
            flag_ids[name] = len(flag_ids) + 1
        return flag_ids[name]

    for rule in spec.triggers:
        trig = (
            TriggerOnce(comment=rule.name or "")
            if rule.once
            else TriggerContinious(comment=rule.name or "")
        )
        for cond in rule.when:
            trig.add_condition(
                _map_condition(cond, zone_ids, enemy_group_ids, target_ids, flag_id, condition)
            )
        for act in rule.then:
            trig.add_action(
                _map_action(
                    act,
                    mission,
                    spec,
                    flag_id,
                    action,
                    enemy_group_ids,
                    target_ids,
                )
            )
        mission.triggerrules.triggers.append(trig)


def _map_condition(cond, zone_ids, enemy_group_ids, target_group_ids, flag_id, condition_mod):
    if isinstance(cond, TimeMoreCondition):
        return condition_mod.TimeAfter(int(cond.seconds))
    if isinstance(cond, FlagIsCondition):
        fid = flag_id(cond.flag)
        return condition_mod.FlagIsTrue(fid) if cond.value else condition_mod.FlagIsFalse(fid)
    if isinstance(cond, UnitDeadCondition):
        if cond.enemy_index >= len(enemy_group_ids):
            raise ValueError(
                f"unit_dead enemy_index {cond.enemy_index} has no compiled enemy group "
                f"(have {len(enemy_group_ids)})"
            )
        return condition_mod.GroupDead(enemy_group_ids[cond.enemy_index])
    if isinstance(cond, TargetDeadCondition):
        if cond.target_index >= len(target_group_ids):
            raise ValueError(
                f"target_dead target_index {cond.target_index} has no compiled target group "
                f"(have {len(target_group_ids)})"
            )
        return condition_mod.GroupDead(target_group_ids[cond.target_index])
    if isinstance(cond, CoalitionInZoneCondition):
        zid = zone_ids.get(cond.zone)
        if zid is None:
            raise ValueError(f"Unknown zone {cond.zone!r} at compile time")
        return condition_mod.PartOfCoalitionInZone(cond.coalition.value, zid)
    raise ValueError(f"Unsupported trigger condition type: {type(cond)!r}")


def _resolve_group_id(act, enemy_group_ids: list[int], target_group_ids: list[int]) -> int:
    if act.enemy_index is not None:
        if act.enemy_index >= len(enemy_group_ids):
            raise ValueError(
                f"activate/deactivate enemy_index {act.enemy_index} has no compiled enemy "
                f"group (have {len(enemy_group_ids)})"
            )
        return enemy_group_ids[act.enemy_index]
    assert act.target_index is not None
    if act.target_index >= len(target_group_ids):
        raise ValueError(
            f"activate/deactivate target_index {act.target_index} has no compiled target "
            f"group (have {len(target_group_ids)})"
        )
    return target_group_ids[act.target_index]


def _map_action(
    act,
    mission,
    spec: MissionSpec,
    flag_id,
    action_mod,
    enemy_group_ids: list[int],
    target_group_ids: list[int],
):
    if isinstance(act, MessageAction):
        seconds = int(act.duration_s) if act.duration_s is not None else 10
        # delay_s is Spec-level; ME out-text uses display duration. Spec delay is
        # approximated by requiring time conditions in ``when`` for v1.
        return action_mod.MessageToAll(mission.string(act.text), seconds=max(seconds, 1))
    if isinstance(act, SetFlagAction):
        fid = flag_id(act.flag)
        return action_mod.SetFlag(fid) if act.value else action_mod.ClearFlag(fid)
    if isinstance(act, MissionEndAction):
        if act.result is MissionEndResult.WIN:
            winner = spec.player.coalition.value
        else:
            winner = opposing_coalition(spec.player.coalition).value
        return action_mod.EndMission(winner=winner, text=mission.string(""))
    if isinstance(act, RadioItemAddAction):
        fid = flag_id(act.flag)
        text = mission.string(act.label)
        if act.coalition is not None:
            return action_mod.AddRadioItemForCoalition(
                coalitionlist=act.coalition.value,
                radiotext=text,
                flag=fid,
                value=1,
            )
        return action_mod.AddRadioItem(radiotext=text, flag=fid, value=1)
    if isinstance(act, RadioItemRemoveAction):
        return action_mod.RemoveRadioItem(radiotext=mission.string(act.label))
    if isinstance(act, ActivateGroupAction):
        return action_mod.ActivateGroup(
            group=_resolve_group_id(act, enemy_group_ids, target_group_ids)
        )
    if isinstance(act, DeactivateGroupAction):
        return action_mod.DeactivateGroup(
            group=_resolve_group_id(act, enemy_group_ids, target_group_ids)
        )
    raise ValueError(f"Unsupported trigger action type: {type(act)!r}")


def collect_flag_names(rules: list[TriggerRule]) -> list[str]:
    """Ordered unique flag names (test helper)."""
    seen: list[str] = []
    for rule in rules:
        for cond in rule.when:
            if isinstance(cond, FlagIsCondition) and cond.flag not in seen:
                seen.append(cond.flag)
        for act in rule.then:
            if (
                isinstance(act, SetFlagAction)
                and act.flag not in seen
                or isinstance(act, RadioItemAddAction)
                and act.flag not in seen
            ):
                seen.append(act.flag)
    return seen
