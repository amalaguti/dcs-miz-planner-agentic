"""Opt-in mission dynamics packs → typed triggers (no Lua).

Play-time Layer B (dice / F10 / hybrid), distinct from CLI ``randomize`` (Layer A).
"""

from __future__ import annotations

import re

from .models import (
    ActivateGroupAction,
    DynamicsMenu,
    DynamicsMode,
    DynamicsPool,
    DynamicsRoll,
    DynamicsSpec,
    FlagEqualsCondition,
    FlagIsCondition,
    MessageAction,
    MissionSpec,
    RadioItemAddAction,
    RadioItemRemoveAction,
    SetFlagAction,
    SetFlagRandomAction,
    TimeMoreCondition,
    TriggerRule,
)

_LOCKED_FLAG = "dyn_locked"
_AUTO_FLAG = "dyn_auto"
_POOL_FLAG_PREFIX = "dyn_pool_"
_ID_SAFE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


class DynamicsError(Exception):
    """Structured expand/validation failure for dynamics packs."""

    def __init__(
        self,
        code: str,
        path: str,
        message: str,
        *,
        hint: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message
        self.hint = hint


def expand_dynamics_if_needed(spec: MissionSpec) -> MissionSpec:
    """Return Spec unchanged, or with dynamics materialised into triggers."""
    if spec.dynamics is None:
        return spec
    return apply_dynamics(spec)


def apply_dynamics(spec: MissionSpec) -> MissionSpec:
    """Expand ``dynamics`` into typed triggers; clear the pack afterward."""
    dyn = spec.dynamics
    if dyn is None:
        return spec

    if spec.narrative is not None and spec.narrative.enabled:
        raise DynamicsError(
            "dynamics_narrative_xor",
            "dynamics",
            "dynamics cannot be used together with narrative.enabled",
            hint="Disable narrative, or omit dynamics and keep the narrative pack",
        )

    if spec.zones or spec.triggers:
        raise DynamicsError(
            "dynamics_conflict",
            "dynamics",
            "dynamics cannot be used when zones or triggers are already set",
            hint="Clear zones/triggers, or omit dynamics and keep hand-written rules",
        )

    _validate_pools(spec, dyn)

    if dyn.mode is DynamicsMode.FIXED:
        triggers: list[TriggerRule] = []
    elif dyn.mode is DynamicsMode.LIVE:
        triggers = _expand_live(spec, dyn)
    elif dyn.mode is DynamicsMode.CHOOSE:
        triggers = _expand_choose(spec, dyn)
    elif dyn.mode is DynamicsMode.HYBRID:
        triggers = _expand_hybrid(spec, dyn)
    else:
        raise DynamicsError(
            "dynamics_unsupported_mode",
            "dynamics.mode",
            f"Unsupported dynamics mode {dyn.mode!r}",
        )

    return spec.model_copy(update={"triggers": triggers, "dynamics": None})


def _validate_pools(spec: MissionSpec, dyn: DynamicsSpec) -> None:
    if dyn.mode is DynamicsMode.FIXED:
        return

    if not dyn.pools:
        raise DynamicsError(
            "dynamics_pools_required",
            "dynamics.pools",
            f"dynamics.mode {dyn.mode.value!r} requires a non-empty pools list",
        )

    seen_ids: set[str] = set()
    for i, pool in enumerate(dyn.pools):
        path = f"dynamics.pools[{i}]"
        if not _ID_SAFE.match(pool.id):
            raise DynamicsError(
                "dynamics_pool_id_invalid",
                f"{path}.id",
                (
                    f"pool id {pool.id!r} must start with a letter and contain only "
                    "letters, digits, and underscores"
                ),
            )
        if pool.id in seen_ids:
            raise DynamicsError(
                "dynamics_pool_id_duplicate",
                f"{path}.id",
                f"duplicate dynamics pool id {pool.id!r}",
            )
        seen_ids.add(pool.id)

        for ei, eidx in enumerate(pool.enemy_indices):
            if eidx >= len(spec.enemies):
                raise DynamicsError(
                    "dynamics_enemy_index",
                    f"{path}.enemy_indices[{ei}]",
                    f"enemy_indices {eidx} is out of range (enemies has {len(spec.enemies)})",
                )
            if not spec.enemies[eidx].late_activation:
                raise DynamicsError(
                    "dynamics_enemy_not_late",
                    f"enemies[{eidx}].late_activation",
                    (f"pool {pool.id!r} references enemies[{eidx}] without late_activation: true"),
                    hint="Set late_activation on pooled groups, or use a different index",
                )

        for ti, tidx in enumerate(pool.target_indices):
            if tidx >= len(spec.targets):
                raise DynamicsError(
                    "dynamics_target_index",
                    f"{path}.target_indices[{ti}]",
                    f"target_indices {tidx} is out of range (targets has {len(spec.targets)})",
                )
            if not spec.targets[tidx].late_activation:
                raise DynamicsError(
                    "dynamics_target_not_late",
                    f"targets[{tidx}].late_activation",
                    (f"pool {pool.id!r} references targets[{tidx}] without late_activation: true"),
                    hint="Set late_activation on pooled targets, or use a different index",
                )

        if dyn.mode in (DynamicsMode.LIVE, DynamicsMode.HYBRID) and pool.roll_value is None:
            raise DynamicsError(
                "dynamics_roll_value_required",
                f"{path}.roll_value",
                f"pool {pool.id!r} requires roll_value for mode {dyn.mode.value!r}",
            )
        if dyn.mode in (DynamicsMode.CHOOSE, DynamicsMode.HYBRID) and not pool.menu_label:
            raise DynamicsError(
                "dynamics_menu_label_required",
                f"{path}.menu_label",
                f"pool {pool.id!r} requires menu_label for mode {dyn.mode.value!r}",
            )

    if dyn.mode in (DynamicsMode.LIVE, DynamicsMode.HYBRID):
        roll = _resolved_roll(dyn)
        values = [p.roll_value for p in dyn.pools if p.roll_value is not None]
        if len(values) != len(set(values)):
            raise DynamicsError(
                "dynamics_roll_value_duplicate",
                "dynamics.pools",
                "pool roll_value values must be unique",
            )
        for i, pool in enumerate(dyn.pools):
            assert pool.roll_value is not None
            if pool.roll_value < roll.min or pool.roll_value > roll.max:
                raise DynamicsError(
                    "dynamics_roll_value_range",
                    f"dynamics.pools[{i}].roll_value",
                    (
                        f"roll_value {pool.roll_value} is outside dynamics.roll "
                        f"[{roll.min}, {roll.max}]"
                    ),
                )


def _resolved_roll(dyn: DynamicsSpec) -> DynamicsRoll:
    if dyn.roll is not None:
        return dyn.roll
    values = [p.roll_value for p in dyn.pools if p.roll_value is not None]
    if not values:
        return DynamicsRoll()
    return DynamicsRoll(min=min(values), max=max(values))


def _resolved_menu(dyn: DynamicsSpec) -> DynamicsMenu:
    return dyn.menu if dyn.menu is not None else DynamicsMenu()


def _pool_flag(pool_id: str) -> str:
    return f"{_POOL_FLAG_PREFIX}{pool_id}"


def _activate_actions(pool: DynamicsPool) -> list:
    actions: list = []
    for eidx in pool.enemy_indices:
        actions.append(ActivateGroupAction(enemy_index=eidx))
    for tidx in pool.target_indices:
        actions.append(ActivateGroupAction(target_index=tidx))
    if pool.message:
        actions.append(MessageAction(text=pool.message, duration_s=12))
    return actions


def _exclusive_when_prefix(exclusive: bool) -> list:
    if not exclusive:
        return []
    return [FlagIsCondition(flag=_LOCKED_FLAG, value=False)]


def _exclusive_then_suffix(exclusive: bool, *, radio_labels: list[str]) -> list:
    if not exclusive:
        return []
    actions: list = [SetFlagAction(flag=_LOCKED_FLAG, value=True)]
    for label in radio_labels:
        actions.append(RadioItemRemoveAction(label=label))
    return actions


def _menu_labels(dyn: DynamicsSpec, *, include_auto: bool) -> list[str]:
    menu = _resolved_menu(dyn)
    labels: list[str] = []
    if include_auto:
        labels.append(menu.auto_label)
    for pool in dyn.pools:
        if pool.menu_label:
            labels.append(pool.menu_label)
    return labels


def _expand_live(spec: MissionSpec, dyn: DynamicsSpec) -> list[TriggerRule]:
    del spec  # validated already
    roll = _resolved_roll(dyn)
    triggers: list[TriggerRule] = [
        TriggerRule(
            name="dynamics_roll",
            once=True,
            when=[TimeMoreCondition(seconds=roll.after_s)],
            then=[
                SetFlagRandomAction(flag=roll.flag, min=roll.min, max=roll.max),
            ],
        )
    ]
    for pool in dyn.pools:
        assert pool.roll_value is not None
        when = [
            FlagEqualsCondition(flag=roll.flag, value=pool.roll_value),
            *_exclusive_when_prefix(dyn.exclusive),
        ]
        then = [
            *_activate_actions(pool),
            *_exclusive_then_suffix(dyn.exclusive, radio_labels=[]),
        ]
        triggers.append(
            TriggerRule(
                name=f"dynamics_activate_{pool.id}",
                once=True,
                when=when,
                then=then,
            )
        )
    return triggers


def _expand_choose(spec: MissionSpec, dyn: DynamicsSpec) -> list[TriggerRule]:
    menu = _resolved_menu(dyn)
    coalition = spec.player.coalition
    labels = _menu_labels(dyn, include_auto=False)
    radio_actions = [
        RadioItemAddAction(
            label=pool.menu_label,  # type: ignore[arg-type]
            flag=_pool_flag(pool.id),
            coalition=coalition,
        )
        for pool in dyn.pools
    ]
    triggers: list[TriggerRule] = [
        TriggerRule(
            name="dynamics_radio_menu",
            once=True,
            when=[TimeMoreCondition(seconds=menu.after_s)],
            then=radio_actions,
        )
    ]
    for pool in dyn.pools:
        when = [
            FlagIsCondition(flag=_pool_flag(pool.id), value=True),
            *_exclusive_when_prefix(dyn.exclusive),
        ]
        then = [
            *_activate_actions(pool),
            *_exclusive_then_suffix(dyn.exclusive, radio_labels=labels),
        ]
        triggers.append(
            TriggerRule(
                name=f"dynamics_activate_{pool.id}",
                once=True,
                when=when,
                then=then,
            )
        )
    return triggers


def _expand_hybrid(spec: MissionSpec, dyn: DynamicsSpec) -> list[TriggerRule]:
    roll = _resolved_roll(dyn)
    menu = _resolved_menu(dyn)
    coalition = spec.player.coalition
    labels = _menu_labels(dyn, include_auto=True)

    radio_actions: list = [
        RadioItemAddAction(
            label=menu.auto_label,
            flag=_AUTO_FLAG,
            coalition=coalition,
        )
    ]
    for pool in dyn.pools:
        radio_actions.append(
            RadioItemAddAction(
                label=pool.menu_label,  # type: ignore[arg-type]
                flag=_pool_flag(pool.id),
                coalition=coalition,
            )
        )

    triggers: list[TriggerRule] = [
        TriggerRule(
            name="dynamics_radio_menu",
            once=True,
            when=[TimeMoreCondition(seconds=menu.after_s)],
            then=radio_actions,
        ),
    ]
    auto_then: list = [
        SetFlagRandomAction(flag=roll.flag, min=roll.min, max=roll.max),
    ]
    if dyn.exclusive:
        # Auto claims the lock so menu picks cannot also fire; roll branches
        # still activate (they key off Auto + flag_equals, not unlocked).
        auto_then.append(SetFlagAction(flag=_LOCKED_FLAG, value=True))
        auto_then.extend(RadioItemRemoveAction(label=label) for label in labels)
    triggers.append(
        TriggerRule(
            name="dynamics_auto_roll",
            once=True,
            when=[
                FlagIsCondition(flag=_AUTO_FLAG, value=True),
                *_exclusive_when_prefix(dyn.exclusive),
            ],
            then=auto_then,
        )
    )

    for pool in dyn.pools:
        assert pool.roll_value is not None
        # Menu pick path
        menu_when = [
            FlagIsCondition(flag=_pool_flag(pool.id), value=True),
            *_exclusive_when_prefix(dyn.exclusive),
        ]
        menu_then = [
            *_activate_actions(pool),
            *_exclusive_then_suffix(dyn.exclusive, radio_labels=labels),
        ]
        triggers.append(
            TriggerRule(
                name=f"dynamics_menu_{pool.id}",
                once=True,
                when=menu_when,
                then=menu_then,
            )
        )
        # Dice path (Auto already set dyn_locked when exclusive)
        roll_when = [FlagEqualsCondition(flag=roll.flag, value=pool.roll_value)]
        if dyn.exclusive:
            # Only fire dice activate if Auto ran (locked) and this pool was not
            # chosen via menu — menu paths activate immediately and also lock.
            # Auto sets locked without activating; roll branches activate after.
            roll_when.append(FlagIsCondition(flag=_AUTO_FLAG, value=True))
        triggers.append(
            TriggerRule(
                name=f"dynamics_roll_{pool.id}",
                once=True,
                when=roll_when,
                then=_activate_actions(pool),
            )
        )
    return triggers
