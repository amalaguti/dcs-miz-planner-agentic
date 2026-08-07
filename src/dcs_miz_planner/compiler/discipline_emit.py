"""Emit opt-in player.flight.discipline (moving-zone fail-to-follow)."""

from __future__ import annotations

from typing import Any

from ..models import (
    DisciplineHardAction,
    MissionSpec,
    SectionOrder,
    player_flight_join_up_enabled,
)

# Reserved flags: orders use 800–819; discipline uses 820–839.
_FLAG_ARMED = 820
_FLAG_OUTSIDE = 821
_FLAG_SOFT_DONE = 822
_FLAG_HARD_DONE = 823
_FLAG_REJOIN_ORDER = 801  # section_orders_emit REJOIN

_AIRBORNE_AGL_M = 150


def apply_flight_discipline(
    mission: Any,
    spec: MissionSpec,
    *,
    player_group: Any,
    lead_group: Any | None,
    airport: Any,
) -> None:
    """Emit moving bubble + soft/hard progressive beats when discipline is armed."""
    flight = spec.player.flight
    if flight is None or flight.discipline is None:
        return
    if not player_flight_join_up_enabled(flight) or lead_group is None:
        return

    from dcs import action, condition
    from dcs.task import Land
    from dcs.triggers import TriggerContinious, TriggerOnce

    disc = flight.discipline
    player_unit = player_group.units[0]
    lead_unit = lead_group.units[0]

    zone = mission.triggers.add_triggerzone(
        lead_unit.position,
        radius=int(disc.radius_m),
        hidden=True,
        name="section_discipline_bubble",
    )

    # Airborne gate — arm discipline only after player is off the deck.
    arm = TriggerOnce(comment="section_discipline_arm")
    arm.add_condition(
        condition.UnitAltitudeHigherAGL(unit=player_unit.id, altitude=_AIRBORNE_AGL_M)
    )
    arm.add_action(action.SetFlag(_FLAG_ARMED))
    mission.triggerrules.triggers.append(arm)

    # Latch outside / clear when back inside (only while armed).
    go_out = TriggerContinious(comment="section_discipline_out")
    go_out.add_condition(condition.FlagIsTrue(_FLAG_ARMED))
    go_out.add_condition(
        condition.UnitOutsideMovingZone(unit=player_unit.id, zone=zone.id, zoneunit=lead_unit.id)
    )
    go_out.add_condition(condition.FlagIsFalse(_FLAG_OUTSIDE))
    go_out.add_action(action.SetFlag(_FLAG_OUTSIDE))
    mission.triggerrules.triggers.append(go_out)

    come_in = TriggerContinious(comment="section_discipline_in")
    come_in.add_condition(condition.FlagIsTrue(_FLAG_ARMED))
    come_in.add_condition(condition.FlagIsTrue(_FLAG_OUTSIDE))
    come_in.add_condition(
        condition.UnitInMovingZone(unit=player_unit.id, zone=zone.id, zoneunit=lead_unit.id)
    )
    come_in.add_action(action.ClearFlag(_FLAG_OUTSIDE))
    mission.triggerrules.triggers.append(come_in)

    # Soft warn after continuous time outside.
    soft = TriggerContinious(comment="section_discipline_soft")
    soft.add_condition(condition.FlagIsTrue(_FLAG_OUTSIDE))
    soft.add_condition(condition.FlagIsFalse(_FLAG_SOFT_DONE))
    soft.add_condition(condition.TimeSinceFlag(flag=_FLAG_OUTSIDE, seconds=int(disc.soft_after_s)))
    soft.add_action(action.SetFlag(_FLAG_SOFT_DONE))
    soft.add_action(
        action.MessageToAll(
            text=mission.string("Section — rejoin / form up. You are off station."),
            seconds=12,
        )
    )
    if SectionOrder.REJOIN in flight.orders:
        soft.add_action(action.SetFlag(_FLAG_REJOIN_ORDER))
    mission.triggerrules.triggers.append(soft)

    # Hard beat after longer continuous time outside (total since OUTSIDE set).
    hard = TriggerContinious(comment="section_discipline_hard")
    hard.add_condition(condition.FlagIsTrue(_FLAG_OUTSIDE))
    hard.add_condition(condition.FlagIsTrue(_FLAG_SOFT_DONE))
    hard.add_condition(condition.FlagIsFalse(_FLAG_HARD_DONE))
    hard.add_condition(condition.TimeSinceFlag(flag=_FLAG_OUTSIDE, seconds=int(disc.hard_after_s)))
    hard.add_action(action.SetFlag(_FLAG_HARD_DONE))

    if disc.hard is DisciplineHardAction.MISSION_END:
        hard.add_action(
            action.MessageToAll(
                text=mission.string("Section discipline — mission aborted. Rejoin failed."),
                seconds=10,
            )
        )
        hard.add_action(action.EndMission(winner="", text=mission.string("")))
    elif disc.hard is DisciplineHardAction.SECTION_RTB:
        lead_group.add_trigger_action(Land(position=airport.position))
        rtb_idx = len(lead_group.tasks)
        hard.add_action(
            action.MessageToAll(
                text=mission.string("Section discipline — lead RTB. Rejoin the recovery."),
                seconds=12,
            )
        )
        hard.add_action(action.AITaskPush(groupid=lead_group.id, task_index=rtb_idx))
    else:
        hard.add_action(
            action.MessageToAll(
                text=mission.string("Section discipline — final warning. Rejoin immediately."),
                seconds=14,
            )
        )
    mission.triggerrules.triggers.append(hard)
