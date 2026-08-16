"""Curated Spec allowlists for Channel validation (fail-left before compile)."""

from __future__ import annotations


def known_countries(era: str | None = None) -> frozenset[str]:
    """Known PyDCS country class names, optionally filtered by packaged era."""
    from .registry import get_channel_registry

    return frozenset(get_channel_registry().list_countries(era=era))


def __getattr__(name: str) -> object:
    if name == "KNOWN_COUNTRIES":
        return known_countries()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# PyDCS ``dcs.unit.Skill`` member names — listed without importing PyDCS at validate time.
KNOWN_SKILLS: frozenset[str] = frozenset(
    {
        "Average",
        "Good",
        "High",
        "Excellent",
        "Player",
        "Client",
        "Random",
    }
)

# Skills allowed for AI wingmen / lead mates on ``player.flight`` (no Player/Client).
AI_FLIGHT_SKILLS: frozenset[str] = frozenset(KNOWN_SKILLS - {"Player", "Client"})

_COUNTRY_HINTS: dict[str, str] = {
    "Germany": "Channel Axis aircraft use country ThirdReich (Germany is modern blue in PyDCS)",
}


def country_hint(name: str, era: str | None = None) -> str | None:
    countries = known_countries(era=era)
    return _COUNTRY_HINTS.get(name) or (
        f"Known countries: {', '.join(sorted(countries))}" if name not in countries else None
    )


def skill_hint(name: str) -> str:
    return f"Known skills: {', '.join(sorted(KNOWN_SKILLS))}"


def ai_flight_skill_hint(name: str) -> str:
    return f"AI flight skills: {', '.join(sorted(AI_FLIGHT_SKILLS))}"
