"""Apply optional GroundTarget motion as native ME ship/vehicle waypoints.

Speed bands come from packaged ``target_motion.yaml`` (not PyDCS). Cruise is
picked inside [min, max] per mission (seeded); waypoints jitter around cruise.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any

import yaml

from .models import GroundTarget, MissionSpec, TargetMotion, ground_target_motion

_PATROL_HEADINGS_DEG = (0.0, 90.0, 180.0, 270.0)
# Within-mission pacing around cruise (path/patrol legs).
_WAYPOINT_SPEED_FACTORS = (0.85, 1.0, 1.15, 0.75, 1.05)
# ME Disperse Under Fire default when moving on land (seconds).
_DEFAULT_DISPERSE_UNDER_FIRE_S = 180


@dataclass(frozen=True)
class SpeedProfile:
    id: str
    label: str
    min_kmh: float
    max_kmh: float

    def clamp(self, speed_kmh: float) -> float:
        return max(self.min_kmh, min(self.max_kmh, float(speed_kmh)))


@lru_cache(maxsize=1)
def _load_motion_tables() -> tuple[dict[str, SpeedProfile], dict[str, str]]:
    root = resources.files("dcs_miz_planner.data") / "era" / "wwii"
    data = yaml.safe_load((root / "target_motion.yaml").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("target_motion.yaml must be a mapping")
    profiles_raw = data.get("profiles") or {}
    units_raw = data.get("units") or {}
    profiles: dict[str, SpeedProfile] = {}
    for pid, meta in profiles_raw.items():
        if not isinstance(meta, dict):
            raise TypeError(f"target_motion.yaml profiles.{pid} must be a mapping")
        profiles[str(pid)] = SpeedProfile(
            id=str(pid),
            label=str(meta.get("label") or pid),
            min_kmh=float(meta["min_kmh"]),
            max_kmh=float(meta["max_kmh"]),
        )
        if profiles[str(pid)].min_kmh > profiles[str(pid)].max_kmh:
            raise ValueError(f"target_motion.yaml profiles.{pid}: min_kmh > max_kmh")
    units = {str(k): str(v) for k, v in units_raw.items()}
    return profiles, units


def speed_profile_for_unit(unit_id: str, *, domain: str) -> SpeedProfile:
    profiles, units = _load_motion_tables()
    pid = units.get(unit_id)
    if pid is None:
        pid = "default_sea" if domain == "sea" else "default_land"
    if pid not in profiles:
        raise ValueError(f"Unknown motion profile {pid!r} for unit {unit_id!r}")
    return profiles[pid]


def motion_seed_for_spec(spec: MissionSpec) -> int:
    """Stable seed for per-mission speed picks (weather seed or name hash)."""
    if spec.weather_opts is not None:
        return int(spec.weather_opts.seed)
    digest = hashlib.sha256(spec.name.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def resolve_cruise_kmh(
    tgt: GroundTarget,
    *,
    domain: str,
    seed: int,
    target_index: int,
) -> float:
    """Cruise speed in km/h: Spec override (clamped) or seeded pick in profile band."""
    profile = speed_profile_for_unit(tgt.unit, domain=domain)
    if tgt.speed_kmh is not None:
        return profile.clamp(tgt.speed_kmh)
    unit_mix = int(hashlib.sha256(tgt.unit.encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random((seed ^ (target_index * 0x9E3779B9) ^ unit_mix) & 0xFFFFFFFF)
    # Inclusive-ish band; round to 0.5 km/h for stable ME values.
    raw = rng.uniform(profile.min_kmh, profile.max_kmh)
    return round(raw * 2) / 2.0


def waypoint_speeds_kmh(
    cruise_kmh: float, *, count: int, seed: int, target_index: int
) -> list[float]:
    """Per-waypoint speeds around cruise (within-mission variation)."""
    if count <= 0:
        return []
    rng = random.Random((seed ^ 0xA5A5A5A5 ^ (target_index << 7)) & 0xFFFFFFFF)
    # Rotate factor start so missions differ.
    offset = rng.randrange(len(_WAYPOINT_SPEED_FACTORS))
    out: list[float] = []
    for i in range(count):
        factor = _WAYPOINT_SPEED_FACTORS[(offset + i) % len(_WAYPOINT_SPEED_FACTORS)]
        out.append(round(cruise_kmh * factor * 2) / 2.0)
    return out


def spawn_position_for_target(
    *,
    airport_position,
    area_center,
    tgt: GroundTarget,
    fallback_pos,
):
    """Initial group position: first path point, first patrol corner, or fallback."""
    motion = ground_target_motion(tgt)
    if motion is TargetMotion.PATH:
        p0 = tgt.path[0]
        return airport_position.point_from_heading(p0.bearing_deg, p0.distance_km * 1000.0)
    if motion is TargetMotion.PATROL:
        assert tgt.patrol_radius_m is not None
        return area_center.point_from_heading(_PATROL_HEADINGS_DEG[0], float(tgt.patrol_radius_m))
    return fallback_pos


def resolve_disperse_under_fire_s(tgt: GroundTarget, *, domain: str) -> int | None:
    """Seconds for OptDisparseUnderFire, or None to skip.

    Ground AI only. Moving land defaults to 180s; ``0`` disables; explicit N uses N.
    Static land only if Spec sets a positive duration.
    """
    if domain != "land":
        return None
    if tgt.disperse_under_fire_s is not None:
        if tgt.disperse_under_fire_s == 0:
            return None
        return int(tgt.disperse_under_fire_s)
    if ground_target_motion(tgt) is TargetMotion.STATIC:
        return None
    return _DEFAULT_DISPERSE_UNDER_FIRE_S


def apply_disperse_under_fire(group: Any, seconds: int) -> None:
    """Attach Disperse Under Fire (option 8) on the group's first waypoint."""
    from dcs.task import OptDisparseUnderFire

    if not group.points:
        return
    group.points[0].add_task(OptDisparseUnderFire(int(seconds)))


def apply_target_motion(
    group,
    *,
    airport_position,
    area_center,
    tgt: GroundTarget,
    domain: str,
    seed: int = 0,
    target_index: int = 0,
) -> None:
    """Append looping waypoints for patrol/path; apply disperse + AI options."""
    from dcs.task import SwitchWaypoint

    from .target_ai import apply_target_ai_options, resolve_target_ai

    resolved_ai = resolve_target_ai(tgt)
    land_formation = resolved_ai.move_formation if domain == "land" else None

    motion = ground_target_motion(tgt)
    if motion is not TargetMotion.STATIC:
        cruise = resolve_cruise_kmh(tgt, domain=domain, seed=seed, target_index=target_index)
        profile = speed_profile_for_unit(tgt.unit, domain=domain)

        if motion is TargetMotion.PATROL:
            assert tgt.patrol_radius_m is not None
            radius = float(tgt.patrol_radius_m)
            # Group already spawned at heading 0; add remaining corners.
            extra_headings = _PATROL_HEADINGS_DEG[1:]
            speeds = waypoint_speeds_kmh(
                cruise, count=1 + len(extra_headings), seed=seed, target_index=target_index
            )
            speeds = [profile.clamp(s) for s in speeds]
            _set_point_speed_kmh(group.points[0], speeds[0])
            for heading, spd in zip(extra_headings, speeds[1:], strict=True):
                _add_wp(
                    group,
                    area_center.point_from_heading(heading, radius),
                    domain=domain,
                    speed_kmh=spd,
                    move_formation=land_formation,
                )
        else:
            extra = list(tgt.path[1:])
            speeds = waypoint_speeds_kmh(
                cruise, count=1 + len(extra), seed=seed, target_index=target_index
            )
            speeds = [profile.clamp(s) for s in speeds]
            _set_point_speed_kmh(group.points[0], speeds[0])
            for pt, spd in zip(extra, speeds[1:], strict=True):
                _add_wp(
                    group,
                    airport_position.point_from_heading(pt.bearing_deg, pt.distance_km * 1000.0),
                    domain=domain,
                    speed_kmh=spd,
                    move_formation=land_formation,
                )

        n = len(group.points)
        if n >= 2:
            # Loop: last WP → first (DCS waypoint indices are 1-based).
            group.points[-1].add_task(SwitchWaypoint(from_waypoint=n, to_waypoint=1))

    disperse_s = resolve_disperse_under_fire_s(tgt, domain=domain)
    if disperse_s is not None:
        apply_disperse_under_fire(group, disperse_s)

    if resolved_ai.has_emit():
        apply_target_ai_options(group, resolved_ai, domain=domain)


def _set_point_speed_kmh(point: Any, speed_kmh: float) -> None:
    point.speed = float(speed_kmh) / 3.6


def _add_wp(
    group: Any,
    position: Any,
    *,
    domain: str,
    speed_kmh: float,
    move_formation=None,
) -> None:
    from dcs.point import PointAction

    from .models import TargetMoveFormation
    from .target_ai import point_action_for_formation

    if domain == "sea":
        group.add_waypoint(position, speed=speed_kmh)
        return
    action = PointAction.OffRoad
    if isinstance(move_formation, TargetMoveFormation):
        action = point_action_for_formation(move_formation)
    group.add_waypoint(position, speed=speed_kmh, move_formation=action)
