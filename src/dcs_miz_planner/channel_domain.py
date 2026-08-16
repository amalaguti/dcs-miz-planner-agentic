"""Land vs sea probe for strike placement (validate + randomize).

Uses PyDCS airport geometry — not DCS runtime land.getSurfaceType.
Heuristic: near a curated airport ⇒ land; roughly on the UK–opposite-coast
chord ⇒ sea. TheChannel uses UK–FR Channel ids; Normandy uses UK–Cotentin ids.
Other theatres fail closed before a chord runs.
"""

from __future__ import annotations

from typing import Literal

from .models import MissionSpec
from .registry import ChannelRegistry, get_channel_registry

Domain = Literal["land", "sea"]

CHANNEL_THEATRE = "TheChannel"
NORMANDY_THEATRE = "Normandy"

# Channel WWII coastal clusters (PyDCS TheChannel airport ids).
_UK_AIRPORT_IDS: frozenset[int] = frozenset({5, 6, 7, 8, 10, 12, 13, 14})
_FR_AIRPORT_IDS: frozenset[int] = frozenset({1, 2, 3, 4})  # Abbeville…Dunkirk

# Normandy curated clusters (PyDCS Normandy airport ids; not Channel ids).
_NORMANDY_UK_AIRPORT_IDS: frozenset[int] = frozenset({28, 27, 29, 30, 31})
_NORMANDY_FR_AIRPORT_IDS: frozenset[int] = frozenset({4, 1, 19})  # Maupertus, SPD, Carpiquet

_NEAR_AIRPORT_M = 3000.0
_CHORD_SLACK_M = 8000.0

_DOMAIN_THEATRES: frozenset[str] = frozenset({CHANNEL_THEATRE, NORMANDY_THEATRE})


class DomainUnsupportedTheatre(ValueError):
    """Raised when land/sea domain checks are requested off supported theatres."""

    code = "domain_unsupported_theatre"


def domain_supported(theatre: str) -> bool:
    return theatre in _DOMAIN_THEATRES


def require_channel_domain(theatre: str) -> None:
    if not domain_supported(theatre):
        raise DomainUnsupportedTheatre(
            f"Land/sea domain checks are not supported for theatre {theatre!r}"
        )


def _classify_uk_fr_chord(
    theatre: str,
    x: float,
    y: float,
    uk_ids: frozenset[int],
    fr_ids: frozenset[int],
) -> Domain:
    from dcs.mapping import Point

    from .theatre_terrain import terrain_for_theatre

    terrain = terrain_for_theatre(theatre)
    point = Point(x, y, terrain)
    uk = [a for a in terrain.airport_list() if a.id in uk_ids]
    fr = [a for a in terrain.airport_list() if a.id in fr_ids]
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


def classify_channel_domain(x: float, y: float) -> Domain:
    """Return ``land`` or ``sea`` for a Channel terrain map point (x, y).

    Callers that have a Spec theatre MUST use :func:`classify_domain_for_theatre`
    so non-Channel maps fail closed instead of running the UK–FR chord.
    """
    return _classify_uk_fr_chord(CHANNEL_THEATRE, x, y, _UK_AIRPORT_IDS, _FR_AIRPORT_IDS)


def classify_normandy_domain(x: float, y: float) -> Domain:
    """Return ``land`` or ``sea`` for a Normandy terrain map point (x, y)."""
    return _classify_uk_fr_chord(
        NORMANDY_THEATRE,
        x,
        y,
        _NORMANDY_UK_AIRPORT_IDS,
        _NORMANDY_FR_AIRPORT_IDS,
    )


def classify_domain_for_theatre(theatre: str, x: float, y: float) -> Domain:
    """Classify land/sea for ``theatre``; fail closed unless Channel or Normandy."""
    require_channel_domain(theatre)
    if theatre == NORMANDY_THEATRE:
        return classify_normandy_domain(x, y)
    return classify_channel_domain(x, y)


def strike_map_point(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> tuple[float, float]:
    """Compile-equivalent strike Point (x, y) from player airfield + strike block."""
    if spec.strike is None:
        raise ValueError("strike block required")
    return airfield_relative_map_point(
        spec,
        bearing_deg=spec.strike.bearing_deg,
        distance_km=spec.strike.distance_km,
        registry=registry,
    )


def recon_map_point(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> tuple[float, float]:
    """Compile-equivalent recon AOI centre Point (x, y)."""
    if spec.recon is None:
        raise ValueError("recon block required")
    return airfield_relative_map_point(
        spec,
        bearing_deg=spec.recon.bearing_deg,
        distance_km=spec.recon.distance_km,
        registry=registry,
    )


def airfield_relative_map_point(
    spec: MissionSpec,
    *,
    bearing_deg: float,
    distance_km: float,
    registry: ChannelRegistry | None = None,
) -> tuple[float, float]:
    """Map point from player airfield + bearing/distance (same math as CAP/strike/recon)."""
    from .theatre_terrain import terrain_for_theatre

    registry = registry if registry is not None else get_channel_registry()
    terrain = terrain_for_theatre(spec.theatre)
    airdrome_id = registry.airdrome_id(spec.player.airfield, theatre=spec.theatre)
    airport = terrain.airport_by_id(airdrome_id)
    if airport is None:
        raise ValueError(f"Unknown airdromeId {airdrome_id} for {spec.player.airfield}")
    point = airport.position.point_from_heading(bearing_deg, distance_km * 1000.0)
    return float(point.x), float(point.y)


def strike_domain_for_spec(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> Domain:
    require_channel_domain(spec.theatre)
    x, y = strike_map_point(spec, registry=registry)
    return classify_domain_for_theatre(spec.theatre, x, y)


def recon_domain_for_spec(
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> Domain:
    require_channel_domain(spec.theatre)
    x, y = recon_map_point(spec, registry=registry)
    return classify_domain_for_theatre(spec.theatre, x, y)
