"""Land vs sea probe for strike placement (validate + randomize).

Uses PyDCS airport geometry — not DCS runtime land.getSurfaceType.
Heuristic: near a curated airport ⇒ land; TheChannel/Normandy use a
UK–opposite-coast chord ⇒ sea; Caucasus uses a west-of-coast seaward sector;
Syria uses per-coastal seaward windows (Incirlik 165–195°, Bassel/Beirut
225–315° only); Nevada is desert-default land on eight curated AFs.
Falklands and other theatres fail closed before a recipe runs.
"""

from __future__ import annotations

from typing import Literal

from .models import MissionSpec
from .registry import ChannelRegistry, get_channel_registry

Domain = Literal["land", "sea"]

CHANNEL_THEATRE = "TheChannel"
NORMANDY_THEATRE = "Normandy"
CAUCASUS_THEATRE = "Caucasus"
SYRIA_THEATRE = "Syria"
NEVADA_THEATRE = "Nevada"

# Channel WWII coastal clusters (PyDCS TheChannel airport ids).
_UK_AIRPORT_IDS: frozenset[int] = frozenset({5, 6, 7, 8, 10, 12, 13, 14})
_FR_AIRPORT_IDS: frozenset[int] = frozenset({1, 2, 3, 4})  # Abbeville…Dunkirk

# Normandy curated clusters (PyDCS Normandy airport ids; not Channel ids).
_NORMANDY_UK_AIRPORT_IDS: frozenset[int] = frozenset({28, 27, 29, 30, 31})
_NORMANDY_FR_AIRPORT_IDS: frozenset[int] = frozenset({4, 1, 19})  # Maupertus, SPD, Carpiquet

_NEAR_AIRPORT_M = 3000.0
_CHORD_SLACK_M = 8000.0

# Caucasus coastal vs inland clusters (PyDCS Caucasus airport ids; not Channel/Normandy).
_CAUCASUS_COASTAL_IDS: frozenset[int] = frozenset({22, 24, 18})  # Batumi, Kobuleti, Sochi-Adler
_CAUCASUS_INLAND_IDS: frozenset[int] = frozenset(
    {23, 25, 29, 31, 28}
)  # Senaki, Kutaisi, Tbilisi, Vaziani, Mozdok
_CAUCASUS_SEAWARD_MIN_DEG = 225.0  # 270° ± 45° from nearest coastal AF
_CAUCASUS_SEAWARD_MAX_DEG = 315.0

# Syria coastal vs inland clusters (PyDCS Syria airport ids; not Caucasus/Channel).
# Do not promote Adana Şakirpaşa id 2.
_SYRIA_COASTAL_IDS: frozenset[int] = frozenset({16, 21, 6})  # Incirlik, Bassel, Beirut
_SYRIA_INLAND_IDS: frozenset[int] = frozenset(
    {27, 28, 7, 30, 19}
)  # Aleppo, Palmyra, Damascus, Ramat David, King Hussein
_SYRIA_INCIRLIK_ID = 16
_SYRIA_INCIRLIK_SEAWARD_MIN_DEG = 165.0  # 180° ± 15° — not 270±45 (Adana land)
_SYRIA_INCIRLIK_SEAWARD_MAX_DEG = 195.0
_SYRIA_MED_COASTAL_IDS: frozenset[int] = frozenset({21, 6})  # Bassel / Beirut ONLY
_SYRIA_MED_SEAWARD_MIN_DEG = 225.0
_SYRIA_MED_SEAWARD_MAX_DEG = 315.0

# Nevada curated AFs only (PyDCS Nevada airport ids; not Channel/Syria).
# Do not promote Echo Bay / Lake Mead id 7.
_NEVADA_CURATED_IDS: frozenset[int] = frozenset(
    {4, 2, 1, 18, 15, 8, 6, 13}
)  # Nellis, GroomLake, Creech, TonopahTestRange, NorthLasVegas,
# HendersonExecutive, BoulderCity, Mesquite

_DOMAIN_THEATRES: frozenset[str] = frozenset(
    {CHANNEL_THEATRE, NORMANDY_THEATRE, CAUCASUS_THEATRE, SYRIA_THEATRE, NEVADA_THEATRE}
)


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


def classify_caucasus_domain(x: float, y: float) -> Domain:
    """Return ``land`` or ``sea`` for a Caucasus terrain map point (x, y).

    Not a Batumi–Kutaisi chord (that heading is over Colchis land). Near a
    curated airfield ⇒ land. Else if the nearest curated field is inland ⇒
    land. Else if the nearest is coastal and the heading from that field is
    west (270° ± 45°) ⇒ sea. Else land. Sochi-due-south water is a known gap.
    """
    from dcs.mapping import Point

    from .theatre_terrain import terrain_for_theatre

    terrain = terrain_for_theatre(CAUCASUS_THEATRE)
    point = Point(x, y, terrain)
    curated_ids = _CAUCASUS_COASTAL_IDS | _CAUCASUS_INLAND_IDS
    airports = [a for a in terrain.airport_list() if a.id in curated_ids]
    if not airports:
        return "land"
    nearest = min(airports, key=lambda a: point.distance_to_point(a.position))
    if point.distance_to_point(nearest.position) <= _NEAR_AIRPORT_M:
        return "land"
    if nearest.id in _CAUCASUS_INLAND_IDS:
        return "land"
    heading = float(nearest.position.heading_between_point(point)) % 360.0
    if _CAUCASUS_SEAWARD_MIN_DEG <= heading <= _CAUCASUS_SEAWARD_MAX_DEG:
        return "sea"
    return "land"


def _syria_heading_is_seaward(airport_id: int, heading: float) -> bool:
    """Incirlik 165–195°; Bassel/Beirut 225–315° only — never apply Med window to Incirlik."""
    heading = heading % 360.0
    if airport_id == _SYRIA_INCIRLIK_ID:
        return _SYRIA_INCIRLIK_SEAWARD_MIN_DEG <= heading <= _SYRIA_INCIRLIK_SEAWARD_MAX_DEG
    if airport_id in _SYRIA_MED_COASTAL_IDS:
        return _SYRIA_MED_SEAWARD_MIN_DEG <= heading <= _SYRIA_MED_SEAWARD_MAX_DEG
    return False


def classify_syria_domain(x: float, y: float) -> Domain:
    """Return ``land`` or ``sea`` for a Syria terrain map point (x, y).

    Not an Incirlik–Aleppo chord (that heading is over Levant land) and not
    Caucasus 270±45 on Incirlik (west is nearer Adana Şakirpaşa id 2, land).
    Near a curated airfield ⇒ land. Else if the nearest curated field is
    inland ⇒ land. Else if the nearest is coastal and the heading from that
    field is seaward (Incirlik 165–195°; Bassel/Beirut 225–315° only) ⇒ sea.
    Else land.
    """
    from dcs.mapping import Point

    from .theatre_terrain import terrain_for_theatre

    terrain = terrain_for_theatre(SYRIA_THEATRE)
    point = Point(x, y, terrain)
    curated_ids = _SYRIA_COASTAL_IDS | _SYRIA_INLAND_IDS
    airports = [a for a in terrain.airport_list() if a.id in curated_ids]
    if not airports:
        return "land"
    nearest = min(airports, key=lambda a: point.distance_to_point(a.position))
    if point.distance_to_point(nearest.position) <= _NEAR_AIRPORT_M:
        return "land"
    if nearest.id in _SYRIA_INLAND_IDS:
        return "land"
    heading = float(nearest.position.heading_between_point(point)) % 360.0
    if _syria_heading_is_seaward(nearest.id, heading):
        return "sea"
    return "land"


def classify_nevada_domain(x: float, y: float) -> Domain:
    """Return ``land`` or ``sea`` for a Nevada terrain map point (x, y).

    Desert-default land — not a Nellis–Creech chord and not Channel /
    Normandy / Caucasus / Syria recipes. Near a curated airfield ⇒ land.
    Else land. Do not promote Echo Bay id 7. Never run other-theatre
    airport ids on Nevada x,y.
    """
    from dcs.mapping import Point

    from .theatre_terrain import terrain_for_theatre

    terrain = terrain_for_theatre(NEVADA_THEATRE)
    point = Point(x, y, terrain)
    airports = [a for a in terrain.airport_list() if a.id in _NEVADA_CURATED_IDS]
    if not airports:
        return "land"
    nearest = min(airports, key=lambda a: point.distance_to_point(a.position))
    if point.distance_to_point(nearest.position) <= _NEAR_AIRPORT_M:
        return "land"
    return "land"


def classify_domain_for_theatre(theatre: str, x: float, y: float) -> Domain:
    """Classify land/sea for ``theatre``; fail closed unless Channel, Normandy, Caucasus, Syria, or Nevada."""
    require_channel_domain(theatre)
    if theatre == NORMANDY_THEATRE:
        return classify_normandy_domain(x, y)
    if theatre == CAUCASUS_THEATRE:
        return classify_caucasus_domain(x, y)
    if theatre == SYRIA_THEATRE:
        return classify_syria_domain(x, y)
    if theatre == NEVADA_THEATRE:
        return classify_nevada_domain(x, y)
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
