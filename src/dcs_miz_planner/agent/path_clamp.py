"""Narrow invent/chat clamp: rewrite land path waypoints onto strike + place deltas.

CLI ``dcs-miz validate`` does not call this — authors keep custom paths.
"""

from __future__ import annotations

from typing import Any

from ..models import GroundTarget, MissionSpec, TargetMotion, TargetPathPoint, ground_target_motion
from ..registry import ChannelRegistry, RegistryError, get_channel_registry

# Fallback matching french_coast_strike_belt.path_point_deltas / convoy example.
_DEFAULT_PATH_DELTAS: tuple[tuple[float, float], ...] = (
    (0.0, 0.0),
    (3.0, 1.0),
    (-3.0, 2.0),
)


def land_path_deltas_from_registry(
    registry: ChannelRegistry | None = None,
) -> tuple[tuple[float, float], ...]:
    """Return (bearing_delta_deg, distance_delta_km) from french_coast place meta."""
    reg = registry or get_channel_registry()
    for opt in reg.list_planning_options():
        if opt.family != "channel_place" or opt.id != "french_coast_strike_belt":
            continue
        raw = (opt.meta or {}).get("path_point_deltas")
        if not isinstance(raw, list) or len(raw) < 2:
            break
        out: list[tuple[float, float]] = []
        for row in raw[:3]:
            if not isinstance(row, dict):
                continue
            out.append(
                (
                    float(row.get("bearing_delta_deg", 0)),
                    float(row.get("distance_delta_km", 0)),
                )
            )
        if len(out) >= 2:
            return tuple(out)
        break
    return _DEFAULT_PATH_DELTAS


def _strike_or_recon_point(spec: MissionSpec) -> tuple[float, float] | None:
    if spec.strike is not None:
        return float(spec.strike.bearing_deg), float(spec.strike.distance_km)
    if spec.recon is not None:
        return float(spec.recon.bearing_deg), float(spec.recon.distance_km)
    return None


def path_from_center_deltas(
    bearing_deg: float,
    distance_km: float,
    deltas: tuple[tuple[float, float], ...],
) -> list[TargetPathPoint]:
    """Build airfield-relative path points from strike/AOI + place deltas."""
    points: list[TargetPathPoint] = []
    for db, dd in deltas:
        points.append(
            TargetPathPoint(
                bearing_deg=(bearing_deg + db) % 360.0,
                distance_km=max(0.1, distance_km + dd),
            )
        )
    return points


def errors_are_land_path_domain_only(errors: list[Any]) -> bool:
    """True when every error is motion_domain_mismatch on a path sample."""
    if not errors:
        return False
    for e in errors:
        code = getattr(e, "code", None) or (e.get("code") if isinstance(e, dict) else None)
        msg = getattr(e, "message", None) or (e.get("message") if isinstance(e, dict) else "") or ""
        if code != "motion_domain_mismatch":
            return False
        if "path[" not in str(msg):
            return False
    return True


def clamp_land_paths(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> tuple[MissionSpec, bool]:
    """Rewrite land-domain path targets to strike-relative place deltas.

    Returns ``(spec, changed)``. Does not alter units, strike, or sea paths.
    """
    center = _strike_or_recon_point(spec)
    if center is None or not spec.targets:
        return spec, False
    bearing_deg, distance_km = center
    reg = registry or get_channel_registry()
    deltas = land_path_deltas_from_registry(reg)
    new_targets: list[GroundTarget] = []
    changed = False
    for tgt in spec.targets:
        if ground_target_motion(tgt) is not TargetMotion.PATH:
            new_targets.append(tgt)
            continue
        try:
            unit = reg.get_strike_unit(tgt.unit)
        except RegistryError:
            new_targets.append(tgt)
            continue
        if unit.domain != "land":
            new_targets.append(tgt)
            continue
        new_path = path_from_center_deltas(bearing_deg, distance_km, deltas)
        new_targets.append(tgt.model_copy(update={"path": new_path}))
        changed = True
    if not changed:
        return spec, False
    return spec.model_copy(update={"targets": new_targets}), True


def _bearing_delta_deg(a: float, b: float) -> float:
    """Smallest absolute bearing difference in degrees."""
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def land_path_diverges_from_strike(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
    max_bearing_delta_deg: float = 10.0,
    max_distance_delta_km: float = 5.0,
) -> bool:
    """True when a land path target has waypoints far from strike/AOI."""
    center = _strike_or_recon_point(spec)
    if center is None or not spec.targets:
        return False
    bearing_deg, distance_km = center
    reg = registry or get_channel_registry()
    for tgt in spec.targets:
        if ground_target_motion(tgt) is not TargetMotion.PATH or not tgt.path:
            continue
        try:
            unit = reg.get_strike_unit(tgt.unit)
        except RegistryError:
            continue
        if unit.domain != "land":
            continue
        for pt in tgt.path:
            if _bearing_delta_deg(float(pt.bearing_deg), bearing_deg) > max_bearing_delta_deg:
                return True
            if abs(float(pt.distance_km) - distance_km) > max_distance_delta_km:
                return True
    return False


def try_clamp_land_paths_if_needed(
    spec: MissionSpec,
    errors: list[Any] | None = None,
    *,
    registry: ChannelRegistry | None = None,
) -> MissionSpec | None:
    """Clamp land paths after domain fail, or when invent path diverges from strike."""
    need = bool(
        (errors and errors_are_land_path_domain_only(errors))
        or land_path_diverges_from_strike(spec, registry=registry)
    )
    if not need:
        return None
    clamped, changed = clamp_land_paths(spec, registry=registry)
    return clamped if changed else None


def try_clamp_after_path_domain_fail(
    spec: MissionSpec,
    errors: list[Any],
    *,
    registry: ChannelRegistry | None = None,
) -> MissionSpec | None:
    """Compat wrapper — prefer ``try_clamp_land_paths_if_needed``."""
    return try_clamp_land_paths_if_needed(spec, errors, registry=registry)
