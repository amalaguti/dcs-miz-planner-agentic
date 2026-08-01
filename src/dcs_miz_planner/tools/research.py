"""Offline fixtures + optional live web research for commander guidance."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

ENV_RESEARCH_LIVE = "DCS_MIZ_RESEARCH_LIVE"

_FREE_FLIGHT_NOTES = [
    {
        "title": "Channel free-flight familiarisation",
        "snippet": (
            "WWII fighter local hops emphasise disciplined start checks, a clear climb-out, "
            "visual lookout near the field, and conservative fuel for recovery. Over-water "
            "Channel flying raises ditching risk if weather or navigation slips."
        ),
        "source": "fixture:channel_free_flight",
    },
    {
        "title": "Spitfire handling reminders",
        "snippet": (
            "Spitfire takeoff and landing demand careful throttle and rudder; leave margin "
            "for swing. Practise gentle turns and energy awareness before aggressive "
            "manoeuvres on a free flight."
        ),
        "source": "fixture:spitfire_handling",
    },
]

_INTERCEPT_NOTES = [
    {
        "title": "Fighter intercept doctrine (period)",
        "snippet": (
            "Classic fighter intercepts seek altitude and sun advantage before the merge, "
            "pair discipline, and a clean bounce. Break off when outnumbered; do not chase "
            "into flak or cloud without a plan."
        ),
        "source": "fixture:intercept_doctrine",
    },
    {
        "title": "Channel fighter pilot accounts",
        "snippet": (
            "Period accounts stress early tally calls, watching for escorts above bombers, "
            "and fuel/navigation discipline over the Channel after a turning fight."
        ),
        "source": "fixture:channel_pilot_accounts",
    },
]

_GENERIC_NOTES = [
    {
        "title": "WWII fighter briefing themes",
        "snippet": (
            "Brief tactics for the task, rehearse procedures from start to recovery, and "
            "call out weather, fuel, and lookout as primary watch-outs."
        ),
        "source": "fixture:generic_fighter_brief",
    },
]


def fixture_notes(
    *,
    query: str = "",
    mission_type: str | None = None,
) -> list[dict[str, str]]:
    """Canned Channel Spitfire-relevant notes (no network)."""
    mt = (mission_type or "").strip().lower()
    q = (query or "").lower()
    if mt == "intercept" or "intercept" in q or "bandit" in q or "bf-109" in q:
        return list(_INTERCEPT_NOTES)
    if mt == "free_flight" or "free flight" in q or "familiarisation" in q:
        return list(_FREE_FLIGHT_NOTES)
    if "intercept" in q:
        return list(_INTERCEPT_NOTES)
    return list(_GENERIC_NOTES) + list(_FREE_FLIGHT_NOTES)[:1]


def _live_enabled(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return (os.environ.get(ENV_RESEARCH_LIVE) or "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _duckduckgo_notes(query: str, *, timeout_s: float = 3.0) -> list[dict[str, str]]:
    """Best-effort DuckDuckGo Instant Answer snippets; may return empty."""
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1",
        }
    )
    url = f"https://api.duckduckgo.com/?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "dcs-miz-planner/0.1 (research_guidance)"},
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    notes: list[dict[str, str]] = []
    abstract = (payload.get("AbstractText") or "").strip()
    if abstract:
        notes.append(
            {
                "title": (payload.get("Heading") or "Summary").strip() or "Summary",
                "snippet": abstract[:800],
                "source": (payload.get("AbstractURL") or "duckduckgo:abstract").strip(),
            }
        )
    for topic in payload.get("RelatedTopics") or []:
        if not isinstance(topic, dict):
            continue
        text = (topic.get("Text") or "").strip()
        if not text:
            continue
        notes.append(
            {
                "title": text.split(" - ", 1)[0][:120],
                "snippet": text[:800],
                "source": (topic.get("FirstURL") or "duckduckgo:related").strip(),
            }
        )
        if len(notes) >= 5:
            break
    return notes


def gather_research_notes(
    query: str,
    *,
    mission_type: str | None = None,
    theatre: str | None = None,
    aircraft: str | None = None,
    live: bool | None = None,
    web_fetch: Any | None = None,
) -> tuple[list[dict[str, str]], str | None]:
    """
    Return (notes, warning). Never raises for caller soft-fail.

    ``web_fetch`` is injectable for tests (callable returning notes or raising).
    """
    del theatre, aircraft  # reserved for query enrichment / future ranking
    fixtures = fixture_notes(query=query, mission_type=mission_type)
    if not _live_enabled(live):
        return fixtures, None

    fetch = web_fetch or _duckduckgo_notes
    try:
        enriched_q = query.strip()
        if mission_type:
            enriched_q = f"{enriched_q} {mission_type}".strip()
        live_notes = list(fetch(enriched_q))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        return fixtures, f"research live fetch failed: {exc}; using fixtures"
    except Exception as exc:  # noqa: BLE001 — soft-fail any provider bug
        return fixtures, f"research live fetch failed: {exc}; using fixtures"

    if not live_notes:
        return fixtures, "research live returned no snippets; using fixtures"
    # Prefer live snippets; keep one fixture for Channel grounding.
    merged = live_notes + fixtures[:1]
    return merged, None
