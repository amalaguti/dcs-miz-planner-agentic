"""Shared Mission Spec validation — registry + install inventory checks."""

from __future__ import annotations

from dataclasses import dataclass

from .install.models import AvailabilityState, TheatreInventory
from .install.service import get_inventory
from .models import (
    CoalitionInZoneCondition,
    MissionSpec,
    MissionType,
    ObjectiveType,
    UnitDeadCondition,
    opposing_coalition,
)
from .registry import ChannelRegistry, RegistryError, get_channel_registry


def _validate_enemy_aircraft(
    spec: MissionSpec,
    registry: ChannelRegistry,
    errors: list[ValidationError],
) -> None:
    for i, enemy in enumerate(spec.enemies):
        try:
            registry.get_aircraft(enemy.aircraft)
        except RegistryError:
            errors.append(
                ValidationError(
                    code="unknown_aircraft",
                    path=f"enemies[{i}].aircraft",
                    message=f"Unknown aircraft '{enemy.aircraft}'",
                    hint=f"Known: {registry.list_aircraft()}",
                )
            )


def _validate_ground_attack(
    spec: MissionSpec,
    registry: ChannelRegistry,
    errors: list[ValidationError],
) -> None:
    if spec.strike is None:
        errors.append(
            ValidationError(
                code="strike_required",
                path="strike",
                message="ground_attack missions require a nested strike block",
            )
        )
    if not spec.targets:
        errors.append(
            ValidationError(
                code="targets_required",
                path="targets",
                message="ground_attack missions require a non-empty targets list",
            )
        )
    if spec.enemies:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="enemies",
                message="air enemies not supported for ground_attack in schema_version 1",
            )
        )
    if spec.cap is not None:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="cap",
                message="cap not supported for ground_attack: omit the cap block",
            )
        )

    payload_name = (spec.player.payload or "").strip()
    if not payload_name:
        errors.append(
            ValidationError(
                code="payload_required",
                path="player.payload",
                message="ground_attack missions require player.payload (named preset)",
                hint=f"Known: {registry.list_payloads()}",
            )
        )
    else:
        try:
            payload = registry.get_payload(payload_name)
        except RegistryError:
            errors.append(
                ValidationError(
                    code="unknown_payload",
                    path="player.payload",
                    message=f"Unknown payload '{payload_name}'",
                    hint=f"Known: {registry.list_payloads()}",
                )
            )
        else:
            if payload.aircraft != spec.player.aircraft:
                errors.append(
                    ValidationError(
                        code="payload_aircraft_mismatch",
                        path="player.payload",
                        message=(
                            f"Payload '{payload_name}' is for {payload.aircraft!r}, "
                            f"not player aircraft {spec.player.aircraft!r}"
                        ),
                    )
                )

    if not spec.objectives:
        errors.append(
            ValidationError(
                code="objectives_required",
                path="objectives",
                message="ground_attack missions require a non-empty objectives list",
            )
        )
    else:
        if not any(o.type is ObjectiveType.ATTACK_GROUND for o in spec.objectives):
            errors.append(
                ValidationError(
                    code="objectives_required",
                    path="objectives",
                    message="ground_attack missions require at least one attack_ground objective",
                )
            )
        for i, obj in enumerate(spec.objectives):
            if obj.type is not ObjectiveType.ATTACK_GROUND:
                errors.append(
                    ValidationError(
                        code="unknown_objective",
                        path=f"objectives[{i}].type",
                        message=f"Unsupported objective type {obj.type.value!r} for ground_attack",
                        hint="Supported: attack_ground",
                    )
                )

    expected = opposing_coalition(spec.player.coalition)
    practice = bool(spec.strike and spec.strike.practice)
    for i, tgt in enumerate(spec.targets):
        try:
            registry.get_strike_unit(tgt.unit)
        except RegistryError:
            errors.append(
                ValidationError(
                    code="unknown_strike_unit",
                    path=f"targets[{i}].unit",
                    message=f"Unknown strike target '{tgt.unit}'",
                    hint=f"Known: {registry.list_strike_units()}",
                )
            )
        if not practice and tgt.coalition is not expected:
            errors.append(
                ValidationError(
                    code="friendly_target",
                    path=f"targets[{i}].coalition",
                    message=(
                        "Strike targets must be enemy (opposing coalition) only; "
                        f"player is {spec.player.coalition.value}, "
                        f"expected {expected.value}, got {tgt.coalition.value}. "
                        "Set strike.practice true for allied bombing-practice targets."
                    ),
                )
            )


def _validate_escort(
    spec: MissionSpec,
    registry: ChannelRegistry,
    errors: list[ValidationError],
) -> None:
    if spec.escort is None:
        errors.append(
            ValidationError(
                code="escort_required",
                path="escort",
                message="escort missions require a nested escort block",
            )
        )
    if not spec.package:
        errors.append(
            ValidationError(
                code="package_required",
                path="package",
                message="escort missions require a non-empty package list",
            )
        )
    if spec.cap is not None:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="cap",
                message="cap not supported for escort: omit the cap block",
            )
        )
    if spec.strike is not None:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="strike",
                message="strike not supported for escort: omit the strike block",
            )
        )
    if spec.targets:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="targets",
                message="targets not supported for escort: use mission_type ground_attack",
            )
        )
    if spec.player.payload is not None:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="player.payload",
                message="player.payload not supported for escort: omit payload",
            )
        )

    if not spec.objectives:
        errors.append(
            ValidationError(
                code="objectives_required",
                path="objectives",
                message="escort missions require a non-empty objectives list",
            )
        )
    else:
        if not any(o.type is ObjectiveType.ESCORT_PACKAGE for o in spec.objectives):
            errors.append(
                ValidationError(
                    code="objectives_required",
                    path="objectives",
                    message="escort missions require at least one escort_package objective",
                )
            )
        for i, obj in enumerate(spec.objectives):
            if obj.type is not ObjectiveType.ESCORT_PACKAGE:
                errors.append(
                    ValidationError(
                        code="unknown_objective",
                        path=f"objectives[{i}].type",
                        message=f"Unsupported objective type {obj.type.value!r} for escort",
                        hint="Supported: escort_package",
                    )
                )

    for i, flight in enumerate(spec.package):
        try:
            registry.get_aircraft(flight.aircraft)
        except RegistryError:
            errors.append(
                ValidationError(
                    code="unknown_aircraft",
                    path=f"package[{i}].aircraft",
                    message=f"Unknown aircraft '{flight.aircraft}'",
                    hint=f"Known: {registry.list_aircraft()}",
                )
            )
        if flight.coalition is not spec.player.coalition:
            errors.append(
                ValidationError(
                    code="hostile_package",
                    path=f"package[{i}].coalition",
                    message=(
                        "Escort package must be friendly (same coalition as player); "
                        f"player is {spec.player.coalition.value}, "
                        f"got {flight.coalition.value}"
                    ),
                )
            )

    expected_enemy = opposing_coalition(spec.player.coalition)
    for i, enemy in enumerate(spec.enemies):
        if enemy.coalition is not expected_enemy:
            errors.append(
                ValidationError(
                    code="friendly_enemy",
                    path=f"enemies[{i}].coalition",
                    message=(
                        "Escort bounce enemies must oppose the player; "
                        f"expected {expected_enemy.value}, got {enemy.coalition.value}"
                    ),
                )
            )
    _validate_enemy_aircraft(spec, registry, errors)


@dataclass(frozen=True)
class ValidationError:
    """One validation finding."""

    code: str
    message: str
    path: str | None = None
    hint: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of ``validate_mission_spec``."""

    errors: tuple[ValidationError, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors

    def raise_if_errors(self) -> None:
        if self.errors:
            raise MissionValidationError(self)


class MissionValidationError(ValueError):
    """Raised when validation fails and the caller prefers exceptions."""

    def __init__(self, result: ValidationResult) -> None:
        self.result = result
        lines = []
        for err in result.errors:
            loc = f"{err.path}: " if err.path else ""
            hint = f" ({err.hint})" if err.hint else ""
            lines.append(f"{loc}{err.message}{hint}")
        super().__init__("\n".join(lines) if lines else "Mission Spec validation failed")


def _validate_triggers_and_zones(
    spec: MissionSpec,
    errors: list[ValidationError],
) -> None:
    zone_names = {z.name for z in spec.zones}
    if len(zone_names) != len(spec.zones):
        errors.append(
            ValidationError(
                code="duplicate_zone_name",
                path="zones",
                message="zones must have unique names",
            )
        )

    for ti, rule in enumerate(spec.triggers):
        for ci, cond in enumerate(rule.when):
            path = f"triggers[{ti}].when[{ci}]"
            if isinstance(cond, CoalitionInZoneCondition):
                if cond.zone not in zone_names:
                    errors.append(
                        ValidationError(
                            code="unknown_zone",
                            path=f"{path}.zone",
                            message=f"Unknown zone {cond.zone!r}",
                            hint=f"Known zones: {sorted(zone_names) or '(none)'}",
                        )
                    )
            elif isinstance(cond, UnitDeadCondition) and cond.enemy_index >= len(spec.enemies):
                errors.append(
                    ValidationError(
                        code="enemy_index_out_of_range",
                        path=f"{path}.enemy_index",
                        message=(
                            f"enemy_index {cond.enemy_index} out of range "
                            f"(enemies has {len(spec.enemies)} entries)"
                        ),
                    )
                )


def validate_mission_spec(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
    inventory: TheatreInventory | None = None,
    voice: str | None = None,
) -> ValidationResult:
    """Validate a loaded Mission Spec; collect independent errors in one pass."""
    from .narrative import NarrativeError, expand_narrative_if_needed

    try:
        spec = expand_narrative_if_needed(spec, voice=voice)
    except NarrativeError as exc:
        return ValidationResult(
            errors=(
                ValidationError(
                    code=exc.code,
                    path=exc.path,
                    message=exc.message,
                    hint=exc.hint,
                ),
            ),
        )

    registry = registry if registry is not None else get_channel_registry()
    errors: list[ValidationError] = []

    if spec.mission_type not in (
        MissionType.FREE_FLIGHT,
        MissionType.INTERCEPT,
        MissionType.CAP,
        MissionType.GROUND_ATTACK,
        MissionType.ESCORT,
    ):
        errors.append(
            ValidationError(
                code="unsupported_mission_type",
                path="mission_type",
                message=f"Unsupported mission_type {spec.mission_type.value!r}",
                hint="Supported: free_flight, intercept, cap, ground_attack, escort",
            )
        )

    _validate_triggers_and_zones(spec, errors)

    if spec.mission_type is MissionType.FREE_FLIGHT:
        if spec.cap is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="cap",
                    message="cap not supported for free_flight: omit the cap block",
                )
            )
        if spec.strike is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="strike",
                    message="strike not supported for free_flight: omit the strike block",
                )
            )
        if spec.player.payload is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="player.payload",
                    message="player.payload not supported for free_flight: omit payload",
                )
            )
        if spec.escort is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="escort",
                    message="escort not supported for free_flight: omit the escort block",
                )
            )
        for name in ("enemies", "objectives", "targets", "package"):
            if getattr(spec, name):
                errors.append(
                    ValidationError(
                        code="extension_not_supported",
                        path=name,
                        message=(
                            f"{name} not supported for free_flight: must be empty "
                            "(use mission_type intercept, cap, ground_attack, or escort)"
                        ),
                    )
                )
    elif spec.mission_type is MissionType.INTERCEPT:
        if spec.cap is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="cap",
                    message="cap not supported for intercept: omit the cap block",
                )
            )
        if spec.strike is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="strike",
                    message="strike not supported for intercept: omit the strike block",
                )
            )
        if spec.escort is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="escort",
                    message="escort not supported for intercept: omit the escort block",
                )
            )
        if spec.package:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="package",
                    message="package not supported for intercept: use mission_type escort",
                )
            )
        if not spec.enemies:
            errors.append(
                ValidationError(
                    code="enemies_required",
                    path="enemies",
                    message="intercept missions require a non-empty enemies list",
                )
            )
        if not spec.objectives:
            errors.append(
                ValidationError(
                    code="objectives_required",
                    path="objectives",
                    message="intercept missions require a non-empty objectives list",
                )
            )
        for i, obj in enumerate(spec.objectives):
            if obj.type is not ObjectiveType.INTERCEPT_ENEMY:
                errors.append(
                    ValidationError(
                        code="unknown_objective",
                        path=f"objectives[{i}].type",
                        message=f"Unsupported objective type {obj.type.value!r}",
                        hint="Supported: intercept_enemy",
                    )
                )
        _validate_enemy_aircraft(spec, registry, errors)
    elif spec.mission_type is MissionType.CAP:
        if spec.cap is None:
            errors.append(
                ValidationError(
                    code="cap_required",
                    path="cap",
                    message="cap missions require a nested cap block",
                )
            )
        if spec.strike is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="strike",
                    message="strike not supported for cap: omit the strike block",
                )
            )
        if spec.escort is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="escort",
                    message="escort not supported for cap: omit the escort block",
                )
            )
        if spec.package:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="package",
                    message="package not supported for cap: use mission_type escort",
                )
            )
        if not spec.objectives:
            errors.append(
                ValidationError(
                    code="objectives_required",
                    path="objectives",
                    message="cap missions require a non-empty objectives list",
                )
            )
        else:
            if not any(o.type is ObjectiveType.PATROL for o in spec.objectives):
                errors.append(
                    ValidationError(
                        code="objectives_required",
                        path="objectives",
                        message="cap missions require at least one patrol objective",
                    )
                )
            for i, obj in enumerate(spec.objectives):
                if obj.type is not ObjectiveType.PATROL:
                    errors.append(
                        ValidationError(
                            code="unknown_objective",
                            path=f"objectives[{i}].type",
                            message=f"Unsupported objective type {obj.type.value!r} for cap",
                            hint="Supported: patrol",
                        )
                    )
        _validate_enemy_aircraft(spec, registry, errors)
    elif spec.mission_type is MissionType.GROUND_ATTACK:
        if spec.escort is not None:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="escort",
                    message="escort not supported for ground_attack: omit the escort block",
                )
            )
        if spec.package:
            errors.append(
                ValidationError(
                    code="extension_not_supported",
                    path="package",
                    message="package not supported for ground_attack: use mission_type escort",
                )
            )
        _validate_ground_attack(spec, registry, errors)
    elif spec.mission_type is MissionType.ESCORT:
        _validate_escort(spec, registry, errors)

    if not registry.has_theatre(spec.theatre):
        errors.append(
            ValidationError(
                code="unknown_theatre",
                path="theatre",
                message=f"Unsupported theatre '{spec.theatre}'",
                hint=f"Known: {registry.list_theatres()}",
            )
        )
    else:
        inv = inventory if inventory is not None else get_inventory()
        if not inv.dcs_roots:
            errors.append(
                ValidationError(
                    code="install_inventory_unavailable",
                    path="theatre",
                    message="No usable DCS install inventory for theatre availability",
                    hint="Run `dcs-miz theatres --refresh` or pass --dcs-root / set DCS_MIZ_DCS_ROOT",
                )
            )
        else:
            matches = [t for t in inv.theatres if t.theatre_id == spec.theatre]
            available = [
                t for t in matches if t.state is AvailabilityState.AVAILABLE and t.planner_supported
            ]
            if not available:
                if matches:
                    states = sorted({t.state.value for t in matches})
                    errors.append(
                        ValidationError(
                            code="theatre_not_available",
                            path="theatre",
                            message=(
                                f"Theatre '{spec.theatre}' is planner-supported but not "
                                f"locally available (state={states})"
                            ),
                            hint="Enable the map in DCS or run `dcs-miz theatres --refresh`",
                        )
                    )
                else:
                    errors.append(
                        ValidationError(
                            code="theatre_not_available",
                            path="theatre",
                            message=(
                                f"Theatre '{spec.theatre}' not found in local install inventory"
                            ),
                            hint="Install the map or run `dcs-miz theatres --refresh`",
                        )
                    )

    try:
        registry.get_aircraft(spec.player.aircraft)
    except RegistryError:
        errors.append(
            ValidationError(
                code="unknown_aircraft",
                path="player.aircraft",
                message=f"Unknown aircraft '{spec.player.aircraft}'",
                hint=f"Known: {registry.list_aircraft()}",
            )
        )

    try:
        registry.weather_preset(spec.weather.value)
    except RegistryError:
        errors.append(
            ValidationError(
                code="unknown_weather",
                path="weather",
                message=f"Unknown weather preset '{spec.weather.value}'",
                hint=f"Known: {registry.list_weather_presets()}",
            )
        )

    try:
        registry.airdrome_id(spec.player.airfield)
    except RegistryError:
        errors.append(
            ValidationError(
                code="unknown_airfield",
                path="player.airfield",
                message=f"Unknown Channel airfield '{spec.player.airfield}'",
                hint=f"Known: {registry.list_airfields()}",
            )
        )

    return ValidationResult(errors=tuple(errors))
