"""Advisory era/date alignment checks for planned Mission Specs (warnings only)."""

from __future__ import annotations

from ..models import MissionSpec

# Current Channel content (Spitfire / Axis fighters) sits in a WWII historical backdrop.
# Later theatres may use other eras (e.g. Cold War); modern dates stay allowed anytime.
CHANNEL_WWII_ERA_YEAR_MIN = 1939
CHANNEL_WWII_ERA_YEAR_MAX = 1945


def channel_date_realism_warnings(spec: MissionSpec) -> tuple[str, ...]:
    """Warn when Channel date does not match the map's usual historical era."""
    if spec.theatre != "TheChannel":
        return ()
    year = spec.date.year
    if CHANNEL_WWII_ERA_YEAR_MIN <= year <= CHANNEL_WWII_ERA_YEAR_MAX:
        return ()
    return (
        (
            f"Mission date year {year} does not match the usual historical backdrop "
            f"for this Channel content (WWII era, about "
            f"{CHANNEL_WWII_ERA_YEAR_MIN}–{CHANNEL_WWII_ERA_YEAR_MAX}). "
            "The Spec is still valid. Set the date to fit the history you want "
            "(WWII, a later era such as the Cold War when that content exists, "
            "or any modern day if you prefer a free/contemporary flight)."
        ),
    )
