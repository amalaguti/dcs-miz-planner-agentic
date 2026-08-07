"""Curated Spec allowlists for Channel validation (fail-left before compile)."""

from __future__ import annotations

# Channel WWII planner countries (catalog sync + examples). Expand with new theatres.
KNOWN_COUNTRIES: frozenset[str] = frozenset({"UK", "ThirdReich"})

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


def country_hint(name: str) -> str | None:
    return _COUNTRY_HINTS.get(name) or (
        f"Known countries: {', '.join(sorted(KNOWN_COUNTRIES))}"
        if name not in KNOWN_COUNTRIES
        else None
    )


def skill_hint(name: str) -> str:
    return f"Known skills: {', '.join(sorted(KNOWN_SKILLS))}"


def ai_flight_skill_hint(name: str) -> str:
    return f"AI flight skills: {', '.join(sorted(AI_FLIGHT_SKILLS))}"
