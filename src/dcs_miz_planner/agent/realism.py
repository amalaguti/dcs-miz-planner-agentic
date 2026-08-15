"""Advisory era/date alignment checks for planned Mission Specs (warnings only)."""

from __future__ import annotations

from ..models import MissionSpec
from ..registry import RegistryError, get_channel_registry

# WWII historical backdrop for theatres whose packaged era is ``wwii``.
WWII_ERA_YEAR_MIN = 1939
WWII_ERA_YEAR_MAX = 1945

# Backward-compatible aliases (Channel content is WWII).
CHANNEL_WWII_ERA_YEAR_MIN = WWII_ERA_YEAR_MIN
CHANNEL_WWII_ERA_YEAR_MAX = WWII_ERA_YEAR_MAX


def date_realism_warnings(spec: MissionSpec) -> tuple[str, ...]:
    """Warn when Spec date does not match the theatre's packaged era."""
    try:
        era = get_channel_registry().era_for_theatre(spec.theatre)
    except RegistryError:
        return ()
    if era != "wwii":
        return ()
    year = spec.date.year
    if WWII_ERA_YEAR_MIN <= year <= WWII_ERA_YEAR_MAX:
        return ()
    return (
        (
            f"Mission date year {year} does not match the usual historical backdrop "
            f"for this {spec.theatre} content (WWII era, about "
            f"{WWII_ERA_YEAR_MIN}–{WWII_ERA_YEAR_MAX}). "
            "The Spec is still valid. Set the date to fit the history you want "
            "(WWII, a later era such as the Cold War when that content exists, "
            "or any modern day if you prefer a free/contemporary flight)."
        ),
    )


def channel_date_realism_warnings(spec: MissionSpec) -> tuple[str, ...]:
    """Alias — WWII year check is era-keyed (TheChannel and Normandy)."""
    return date_realism_warnings(spec)
