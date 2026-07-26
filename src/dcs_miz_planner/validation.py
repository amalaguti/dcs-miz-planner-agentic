"""Shared Mission Spec validation — registry + install inventory checks."""

from __future__ import annotations

from dataclasses import dataclass

from .install.models import AvailabilityState, TheatreInventory
from .install.service import get_inventory
from .models import MissionSpec, MissionType, ObjectiveType
from .registry import ChannelRegistry, RegistryError, get_channel_registry


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


def validate_mission_spec(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
    inventory: TheatreInventory | None = None,
) -> ValidationResult:
    """Validate a loaded Mission Spec; collect independent errors in one pass."""
    registry = registry if registry is not None else get_channel_registry()
    errors: list[ValidationError] = []

    if spec.mission_type not in (MissionType.FREE_FLIGHT, MissionType.INTERCEPT):
        errors.append(
            ValidationError(
                code="unsupported_mission_type",
                path="mission_type",
                message=f"Unsupported mission_type {spec.mission_type.value!r}",
                hint="Supported: free_flight, intercept",
            )
        )

    if spec.triggers:
        errors.append(
            ValidationError(
                code="extension_not_supported",
                path="triggers",
                message="triggers not supported yet: must be empty in schema_version 1",
            )
        )

    if spec.mission_type is MissionType.FREE_FLIGHT:
        for name in ("enemies", "objectives"):
            if getattr(spec, name):
                errors.append(
                    ValidationError(
                        code="extension_not_supported",
                        path=name,
                        message=(
                            f"{name} not supported for free_flight: must be empty "
                            "(use mission_type intercept)"
                        ),
                    )
                )
    elif spec.mission_type is MissionType.INTERCEPT:
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
