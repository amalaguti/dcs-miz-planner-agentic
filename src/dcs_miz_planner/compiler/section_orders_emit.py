"""Emit curated player.flight.orders as F10 radio + AITaskPush packs."""

from __future__ import annotations

from typing import Any

from ..models import MissionSpec, PlayerFlightRole, SectionOrder

# Reserved numeric flags so Spec hand-triggers (often 1..) do not collide.
_FLAG_BASE = 800

_ORDER_META: dict[SectionOrder, tuple[str, int, str]] = {
    # order -> (F10 label, flag offset, ack message)
    SectionOrder.REJOIN: (
        "Section: Rejoin",
        1,
        "Section — rejoin / form up.",
    ),
    SectionOrder.ENGAGE: (
        "Section: Engage",
        2,
        "Section — weapons free, engage.",
    ),
    SectionOrder.ORBIT: (
        "Section: Orbit",
        3,
        "Section — hold orbit.",
    ),
    SectionOrder.RTB: (
        "Section: RTB",
        4,
        "Section — return to base.",
    ),
    SectionOrder.BREAK: (
        "Section: Break",
        5,
        "Section — break formation, independent.",
    ),
}


def apply_section_orders(
    mission: Any,
    spec: MissionSpec,
    *,
    player_group: Any,
    lead_group: Any | None,
    airport: Any,
) -> None:
    """Register AI triggered actions + F10/flag wiring for ``player.flight.orders``."""
    flight = spec.player.flight
    if flight is None or not flight.orders:
        return

    from dcs import action, condition
    from dcs.mapping import Vector2
    from dcs.task import Follow, Land, OptROE, OrbitAction
    from dcs.triggers import TriggerContinious, TriggerOnce

    ai_group = lead_group if lead_group is not None else player_group
    is_wingman = flight.role is PlayerFlightRole.WINGMAN
    orbit_alt = int(spec.cap.altitude_m) if spec.cap is not None else 3000
    orbit_speed = 400

    # Pre-register AI tasks; remember 1-based indices for AITaskPush.
    task_index: dict[SectionOrder, tuple[Any, int]] = {}

    for order in flight.orders:
        if order is SectionOrder.REJOIN:
            if is_wingman and lead_group is not None:
                # Player re-Follows AI lead.
                player_group.add_trigger_action(
                    Follow(
                        groupid=lead_group.id,
                        group_offset=Vector2(-200.0, 0.0),
                        altitude_difference=-50.0,
                    )
                )
                task_index[order] = (player_group, len(player_group.tasks))
            # Lead same-group: formation is native — F10 message only (no AITaskPush).
            continue
        if order is SectionOrder.ENGAGE:
            ai_group.add_trigger_action(OptROE(OptROE.Values.WeaponFree))
            task_index[order] = (ai_group, len(ai_group.tasks))
            continue
        if order is SectionOrder.ORBIT:
            ai_group.add_trigger_action(
                OrbitAction(
                    altitude=orbit_alt,
                    speed=orbit_speed,
                    pattern=OrbitAction.OrbitPattern.Circle,
                )
            )
            task_index[order] = (ai_group, len(ai_group.tasks))
            continue
        if order is SectionOrder.RTB:
            ai_group.add_trigger_action(Land(position=airport.position))
            task_index[order] = (ai_group, len(ai_group.tasks))
            continue
        if order is SectionOrder.BREAK:
            # Stop current AI tasking (clears Follow/orbit push).
            # Wired via GroupStop action in the flag trigger (no pre-registered task).
            continue

    # Mission-start: add F10 items (blue coalition).
    menu = TriggerOnce(comment="section_orders_menu")
    menu.add_condition(condition.TimeAfter(seconds=1))
    for order in flight.orders:
        label, offset, _msg = _ORDER_META[order]
        fid = _FLAG_BASE + offset
        menu.add_action(
            action.AddRadioItemForCoalition(
                coalitionlist=spec.player.coalition.value,
                radiotext=mission.string(label),
                flag=fid,
                value=1,
            )
        )
    mission.triggerrules.triggers.append(menu)

    # Continuous: flag → clear → message → AI task (or GroupStop for break).
    for order in flight.orders:
        label, offset, msg = _ORDER_META[order]
        fid = _FLAG_BASE + offset
        trig = TriggerContinious(comment=f"section_order_{order.value}")
        trig.add_condition(condition.FlagIsTrue(fid))
        trig.add_action(action.ClearFlag(fid))
        trig.add_action(action.MessageToAll(text=mission.string(msg), seconds=8))
        if order is SectionOrder.BREAK:
            trig.add_action(action.GroupStop(group=ai_group.id))
        elif order in task_index:
            grp, idx = task_index[order]
            trig.add_action(action.AITaskPush(groupid=grp.id, task_index=idx))
        mission.triggerrules.triggers.append(trig)
