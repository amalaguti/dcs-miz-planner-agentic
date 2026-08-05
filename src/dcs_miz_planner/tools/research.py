"""Offline fixtures + optional live web research for commander guidance."""

from __future__ import annotations

import html as html_lib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from html.parser import HTMLParser

ENV_RESEARCH_LIVE = "DCS_MIZ_RESEARCH_LIVE"

# Instant Answer is cheap; HTML fallback needs a bit more headroom on slow links.
_INSTANT_TIMEOUT_S = 4.0
_HTML_TIMEOUT_S = 6.0
# DDG HTML returns an anomaly/challenge page for non-browser User-Agents.
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

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


def enrich_live_query(
    query: str,
    *,
    mission_type: str | None = None,
    theatre: str | None = None,
    aircraft: str | None = None,
    focus: str | None = None,
) -> str:
    """Build a fetch string from the user query plus available Spec context.

    ``focus="mission_design"`` biases toward DCS User Files / public mission repos /
    Mission Editor pattern discovery (still not Spec-field authority).
    """
    parts: list[str] = []
    q = (query or "").strip()
    if q:
        parts.append(q)
    for token in (mission_type, theatre, aircraft):
        t = (token or "").strip()
        if not t:
            continue
        # Avoid duplicating tokens already in the query (case-insensitive).
        if t.lower() in q.lower():
            continue
        parts.append(t)
    # Light WWII/Channel grounding when context suggests Channel ops.
    joined = " ".join(parts).strip()
    lower = joined.lower()
    theatre_l = (theatre or "").strip().lower()
    if (
        ("channel" in lower or theatre_l in {"thechannel", "channel"})
        and "wwii" not in lower
        and "world war" not in lower
    ):
        joined = f"{joined} WWII".strip()

    focus_l = (focus or "").strip().lower()
    if focus_l in {"mission_design", "mission-design", "design"}:
        bias_terms = (
            "DCS World mission",
            "User Files",
            "mission editor triggers",
            "GitHub miz",
        )
        lower2 = joined.lower()
        for term in bias_terms:
            if term.lower() not in lower2:
                joined = f"{joined} {term}".strip()
                lower2 = joined.lower()
    return joined or q


def _http_get(url: str, *, timeout_s: float) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return resp.read()


def _duckduckgo_instant_notes(
    query: str, *, timeout_s: float = _INSTANT_TIMEOUT_S
) -> list[dict[str, str]]:
    """DuckDuckGo Instant Answer snippets; often empty for multi-word queries."""
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1",
        }
    )
    url = f"https://api.duckduckgo.com/?{params}"
    raw = _http_get(url, timeout_s=timeout_s).decode("utf-8").strip()
    if not raw:
        return []
    payload = json.loads(raw)
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


class _DuckDuckGoHtmlResultsParser(HTMLParser):
    """Extract result title + snippet pairs from html.duckduckgo.com markup."""

    def __init__(self) -> None:
        super().__init__()
        self._in_result_a = False
        self._in_snippet = False
        self._title_parts: list[str] = []
        self._snippet_parts: list[str] = []
        self._href: str = ""
        self.results: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: (v or "") for k, v in attrs}
        classes = set((attr.get("class") or "").split())
        if tag == "a" and "result__a" in classes:
            self._in_result_a = True
            self._title_parts = []
            self._href = attr.get("href") or ""
        elif tag in {"a", "td", "div", "span"} and "result__snippet" in classes:
            self._in_snippet = True
            self._snippet_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_result_a:
            self._in_result_a = False
            title = html_lib.unescape("".join(self._title_parts)).strip()
            if title:
                # Flush pending incomplete pair if title arrives before snippet.
                self.results.append(
                    {
                        "title": title[:120],
                        "snippet": "",
                        "source": self._unwrap_ddg_href(self._href) or "duckduckgo:html",
                    }
                )
            self._href = ""
        elif self._in_snippet and tag in {"a", "td", "div", "span"}:
            self._in_snippet = False
            snippet = html_lib.unescape("".join(self._snippet_parts)).strip()
            snippet = re.sub(r"\s+", " ", snippet)
            if self.results and not self.results[-1].get("snippet"):
                self.results[-1]["snippet"] = snippet[:800]
            elif snippet:
                self.results.append(
                    {
                        "title": snippet[:80] or "Result",
                        "snippet": snippet[:800],
                        "source": "duckduckgo:html",
                    }
                )

    def handle_data(self, data: str) -> None:
        if self._in_result_a:
            self._title_parts.append(data)
        elif self._in_snippet:
            self._snippet_parts.append(data)

    @staticmethod
    def _unwrap_ddg_href(href: str) -> str:
        """DDG HTML often wraps destinations as /l/?uddg=<urlencoded>."""
        if not href:
            return ""
        try:
            parsed = urllib.parse.urlparse(href)
            qs = urllib.parse.parse_qs(parsed.query)
            if qs.get("uddg"):
                return qs["uddg"][0]
        except (ValueError, TypeError):
            pass
        if href.startswith("http"):
            return href
        return href


def _duckduckgo_html_notes(
    query: str, *, timeout_s: float = _HTML_TIMEOUT_S
) -> list[dict[str, str]]:
    """Best-effort DuckDuckGo HTML result snippets when Instant Answer is empty."""
    params = urllib.parse.urlencode({"q": query})
    url = f"https://html.duckduckgo.com/html/?{params}"
    raw = _http_get(url, timeout_s=timeout_s).decode("utf-8", errors="replace")
    lower = raw.lower()
    if "anomaly" in lower and "result__a" not in lower:
        raise ValueError("duckduckgo html blocked (anomaly/challenge page)")
    parser = _DuckDuckGoHtmlResultsParser()
    parser.feed(raw)
    notes: list[dict[str, str]] = []
    for item in parser.results:
        snippet = (item.get("snippet") or "").strip()
        title = (item.get("title") or "").strip()
        if not title and not snippet:
            continue
        if not snippet:
            snippet = title
        notes.append(
            {
                "title": title or "Result",
                "snippet": snippet[:800],
                "source": (item.get("source") or "duckduckgo:html").strip(),
            }
        )
        if len(notes) >= 5:
            break
    return notes


def _live_web_notes(query: str) -> list[dict[str, str]]:
    """Cascade: Instant Answer, then HTML results if empty or Instant Answer fails."""
    try:
        notes = _duckduckgo_instant_notes(query)
        if notes:
            return notes
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        # Empty/blocked Instant Answer bodies are common; continue to HTML.
        pass
    return _duckduckgo_html_notes(query)


def is_fixture_source(source: str) -> bool:
    return (source or "").strip().lower().startswith("fixture:")


def gather_research_notes(
    query: str,
    *,
    mission_type: str | None = None,
    theatre: str | None = None,
    aircraft: str | None = None,
    live: bool | None = None,
    focus: str | None = None,
    web_fetch: Callable[[str], list[dict[str, str]]] | None = None,
) -> tuple[list[dict[str, str]], str | None]:
    """
    Return (notes, warning). Never raises for caller soft-fail.

    ``web_fetch`` is injectable for tests (callable returning notes or raising).
    When omitted, live mode uses Instant Answer then HTML fallback.
    ``focus="mission_design"`` enriches the live query toward mission-pattern sources.
    """
    fixtures = fixture_notes(query=query, mission_type=mission_type)
    if not _live_enabled(live):
        return fixtures, None

    fetch = web_fetch or _live_web_notes
    enriched_q = enrich_live_query(
        query,
        mission_type=mission_type,
        theatre=theatre,
        aircraft=aircraft,
        focus=focus,
    )
    try:
        live_notes = list(fetch(enriched_q))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as exc:
        return fixtures, f"research live fetch failed: {exc}; using offline fixtures"
    except Exception as exc:  # noqa: BLE001 — soft-fail any provider bug
        return fixtures, f"research live fetch failed: {exc}; using offline fixtures"

    # Drop empty / fixture-only rows from a buggy provider; treat as empty live.
    live_notes = [
        n
        for n in live_notes
        if (n.get("snippet") or n.get("title")) and not is_fixture_source(n.get("source") or "")
    ]
    if not live_notes:
        return (
            fixtures,
            "research live returned no snippets; using offline fixtures",
        )
    # Prefer live snippets; keep one fixture for Channel grounding.
    merged = live_notes + fixtures[:1]
    return merged, None
