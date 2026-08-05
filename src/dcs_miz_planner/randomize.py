"""Seeded Mission Spec → Spec randomization for replayability.

Draw order when an axis runs (locks determinism for tests):
1. weather — choice among WeatherPreset values
2. time — integer minute delta, then 5-minute snap
3. geometry — for each present block among cap, strike, escort (in that order):
   bearing, distance scale, altitude scale
4. opposition — for each enemies[] entry: count, aircraft, skill
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence

from .models import (
    Cap,
    Escort,
    MissionSpec,
    Strike,
    WeatherPreset,
)
from .registry import RegistryError, get_channel_registry

AXES: tuple[str, ...] = ("weather", "time", "geometry", "opposition")

#: Channel Axis fighters suitable for bounce / intercept opposition (registry ids).
_OPPOSING_FIGHTERS: tuple[str, ...] = ("Bf-109K-4", "FW-190A8", "FW-190D9")
_ENEMY_SKILLS: tuple[str, ...] = ("Average", "Good", "High")

_TIME_JITTER_MIN = 90
_BEARING_JITTER_DEG = 30.0
_DISTANCE_JITTER = 0.20
_ALTITUDE_JITTER = 0.15


class RandomizeError(ValueError):
    """Invalid seed, axes, or randomization input."""


def parse_axes(raw: str | Sequence[str] | None) -> tuple[str, ...]:
    """Parse CLI/tool axes into a validated ordered tuple (subset of AXES)."""
    if raw is None:
        return AXES
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",") if p.strip()]
    else:
        parts = [str(p).strip() for p in raw if str(p).strip()]
    if not parts:
        return AXES
    unknown = sorted({p for p in parts if p not in AXES})
    if unknown:
        raise RandomizeError(f"Unknown randomization axis: {unknown[0]!r}; known: {list(AXES)}")
    # Preserve caller order but unique; still run in canonical AXES order below.
    selected = set(parts)
    return tuple(a for a in AXES if a in selected)


def randomize_mission_spec(
    spec: MissionSpec,
    seed: int,
    axes: str | Sequence[str] | None = None,
    *,
    annotate: bool = False,
) -> MissionSpec:
    """Return a new Spec with seeded variation. Same inputs → same output."""
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        raise RandomizeError("seed must be a non-negative integer")

    selected = parse_axes(axes)
    rng = random.Random(seed)
    out = spec.model_copy(deep=True)

    if "weather" in selected:
        out = out.model_copy(update={"weather": _pick_weather(rng)})
    if "time" in selected:
        out = out.model_copy(update={"start_time": _jitter_time(rng, out.start_time)})
    if "geometry" in selected:
        out = _jitter_geometry(rng, out)
    if "opposition" in selected:
        out = _jitter_opposition(rng, out)

    if annotate:
        note = f"(seed {seed})"
        desc = (out.description or "").rstrip()
        if note not in desc:
            desc = f"{desc}\n\n{note}".strip() if desc else note
            out = out.model_copy(update={"description": desc})

    ensure_finite(out)
    return out


def _pick_weather(rng: random.Random) -> WeatherPreset:
    return rng.choice(list(WeatherPreset))


def _jitter_time(rng: random.Random, start_time: str) -> str:
    hh, mm = (int(p) for p in start_time.split(":"))
    total = hh * 60 + mm
    total = (total + rng.randint(-_TIME_JITTER_MIN, _TIME_JITTER_MIN)) % (24 * 60)
    total = (total // 5) * 5
    return f"{total // 60:02d}:{total % 60:02d}"


def _jitter_geometry(rng: random.Random, spec: MissionSpec) -> MissionSpec:
    updates: dict = {}
    if spec.cap is not None:
        updates["cap"] = _jitter_cap_like(rng, spec.cap)
    if spec.strike is not None:
        updates["strike"] = _jitter_strike(rng, spec)
    if spec.escort is not None:
        updates["escort"] = _jitter_cap_like(rng, spec.escort)
    return spec.model_copy(update=updates) if updates else spec


def _target_domains(spec: MissionSpec) -> set[str]:
    registry = get_channel_registry()
    domains: set[str] = set()
    for tgt in spec.targets:
        try:
            domains.add(registry.get_strike_unit(tgt.unit).domain)
        except RegistryError:
            continue
    return domains


def _strike_domains_ok(spec: MissionSpec, strike: Strike) -> bool:
    from .channel_domain import strike_domain_for_spec

    domains = _target_domains(spec)
    if not domains:
        return True
    candidate = spec.model_copy(update={"strike": strike})
    try:
        point_domain = strike_domain_for_spec(candidate)
    except (ValueError, RegistryError):
        return False
    return domains <= {point_domain}


def _jitter_strike(rng: random.Random, spec: MissionSpec) -> Strike:
    assert spec.strike is not None
    original = spec.strike
    for _ in range(24):
        candidate = _jitter_cap_like(rng, original)
        assert isinstance(candidate, Strike)
        if _strike_domains_ok(spec, candidate):
            return candidate
    return original


def _jitter_cap_like(rng: random.Random, block: Cap | Strike | Escort) -> Cap | Strike | Escort:
    bearing = (block.bearing_deg + rng.uniform(-_BEARING_JITTER_DEG, _BEARING_JITTER_DEG)) % 360.0
    distance = max(
        0.1, block.distance_km * (1.0 + rng.uniform(-_DISTANCE_JITTER, _DISTANCE_JITTER))
    )
    altitude = max(1.0, block.altitude_m * (1.0 + rng.uniform(-_ALTITUDE_JITTER, _ALTITUDE_JITTER)))
    # Keep floats tidy for YAML dumps / equality checks.
    bearing = round(bearing, 3)
    distance = round(distance, 3)
    altitude = round(altitude, 1)
    return block.model_copy(
        update={
            "bearing_deg": bearing,
            "distance_km": distance,
            "altitude_m": altitude,
        }
    )


def _jitter_opposition(rng: random.Random, spec: MissionSpec) -> MissionSpec:
    if not spec.enemies:
        return spec
    fighters = _opposing_fighters()
    skills = list(_ENEMY_SKILLS)
    new_enemies = []
    for enemy in spec.enemies:
        lo = max(1, enemy.count - 1)
        hi = min(16, enemy.count + 2)
        count = rng.randint(lo, hi)
        aircraft = rng.choice(fighters)
        skill = rng.choice(skills)
        new_enemies.append(
            enemy.model_copy(update={"count": count, "aircraft": aircraft, "skill": skill})
        )
    return spec.model_copy(update={"enemies": new_enemies})


def _opposing_fighters() -> list[str]:
    known = set(get_channel_registry().list_aircraft())
    fighters = [a for a in _OPPOSING_FIGHTERS if a in known]
    if not fighters:
        raise RandomizeError("No opposing fighter aircraft available in Channel registry")
    return fighters


def applicable_axes(spec: MissionSpec) -> tuple[str, ...]:
    """Axes that can change something for this Spec (informational)."""
    out: list[str] = ["weather", "time"]
    if spec.cap is not None or spec.strike is not None or spec.escort is not None:
        out.append("geometry")
    if spec.enemies:
        out.append("opposition")
    return tuple(out)


def axes_that_differ(a: MissionSpec, b: MissionSpec) -> list[str]:
    """Which designed axes differ between two Specs (test helper)."""
    diffs: list[str] = []
    if a.weather != b.weather:
        diffs.append("weather")
    if a.start_time != b.start_time:
        diffs.append("time")
    if _geometry_tuple(a) != _geometry_tuple(b):
        diffs.append("geometry")
    if a.enemies != b.enemies:
        diffs.append("opposition")
    return diffs


def _geometry_tuple(spec: MissionSpec) -> tuple:
    def block(b: Cap | Strike | Escort | None) -> tuple | None:
        if b is None:
            return None
        return (b.bearing_deg, b.distance_km, b.altitude_m)

    return (block(spec.cap), block(spec.strike), block(spec.escort))


def ensure_finite(spec: MissionSpec) -> None:
    """Raise if geometry produced non-finite numbers (defensive)."""
    for block in (spec.cap, spec.strike, spec.escort):
        if block is None:
            continue
        for val in (block.bearing_deg, block.distance_km, block.altitude_m):
            if not math.isfinite(val):
                raise RandomizeError("geometry randomization produced a non-finite value")
