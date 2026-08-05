"""Channel map land vs sea probe for strike placement (validate + randomize).

Uses PyDCS TheChannel airport geometry — not DCS runtime land.getSurfaceType.
Heuristic: near a Channel airport ⇒ land; roughly on the UK–FR coastal chord ⇒ sea.
"""

from __future__ import annotations

from typing import Literal

from .models import MissionSpec
from .registry import ChannelRegistry, get_channel_registry

Domain = Literal["land", "sea"]

# Channel WWII coastal clusters (PyDCS TheChannel airport ids).
_UK_AIRPORT_IDS: frozenset[int] = frozenset({5, 6, 7, 8, 10, 12, 13, 14})
_FR_AIRPORT_IDS: frozenset[int] = frozenset({1, 2, 3, 4})  # Abbeville…Dunkirk

_NEAR_AIRPORT_M = 3000.0
_CHORD_SLACK_M = 8000.0


def classify_channel_domain(x: float, y: float) -> Domain:
    """Return ``land`` or ``sea`` for a Channel terrain map point (x, y)."""
    from dcs.mapping import Point

    from .theatre_terrain import terrain_for_theatre

    terrain = terrain_for_theatre("TheChannel")
    point = Point(x, y, terrain)
    uk = [a for a in terrain.airport_list() if a.id in _UK_AIRPORT_IDS]
    fr = [a for a in terrain.airport_list() if a.id in _FR_AIRPORT_IDS]
    if not uk or not fr:
        return "land"
    nearest_uk = min(uk, key=lambda a: point.distance_to_point(a.position))
    nearest_fr = min(fr, key=lambda a: point.distance_to_point(a.position))
    d_uk = point.distance_to_point(nearest_uk.position)
    d_fr = point.distance_to_point(nearest_fr.position)
    d_chord = nearest_uk.position.distance_to_point(nearest_fr.position)
    if min(d_uk, d_fr) <= _NEAR_AIRPORT_M:
        return "land"
    if d_uk + d_fr <= d_chord + _CHORD_SLACK_M:
        return "sea"
    return "land"


def strike_map_point(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> tuple[float, float]:
    """Compile-equivalent strike Point (x, y) from player airfield + strike block."""
    from .theatre_terrain import terrain_for_theatre

    if spec.strike is None:
        raise ValueError("strike block required")
    registry = registry if registry is not None else get_channel_registry()
    terrain = terrain_for_theatre(spec.theatre)
    airdrome_id = registry.airdrome_id(spec.player.airfield)
    airport = terrain.airport_by_id(airdrome_id)
    if airport is None:
        raise ValueError(f"Unknown Channel airdromeId {airdrome_id} for {spec.player.airfield}")
    point = airport.position.point_from_heading(
        spec.strike.bearing_deg, spec.strike.distance_km * 1000.0
    )
    return float(point.x), float(point.y)


def strike_domain_for_spec(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> Domain:
    x, y = strike_map_point(spec, registry=registry)
    return classify_channel_domain(x, y)
