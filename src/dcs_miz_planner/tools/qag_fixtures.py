"""Index gitignored research/ QAG HTML for offline research_guidance colour."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from html.parser import HTMLParser
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

_DATA_PKG = "dcs_miz_planner.data.qag_fixtures"
_INDEX_NAME = "qag_index.yaml"
ENV_RESEARCH_DIR = "DCS_MIZ_RESEARCH_DIR"
_MAX_QAG_NOTES = 3
_MAX_CODE_LABELS = 8
_MAX_LEADS = 2

QAG_DISCLAIMER = (
    "QAG UI names, site templates, and template.lua strings are not Spec or PyDCS "
    "ids — do not copy them into unit_id, aircraft, country, or mission_type."
)

_WWII_THEATRES = frozenset({"thechannel", "channel", "normandy"})
_MODERN_THEATRES = frozenset({"caucasus", "syria", "nevada", "falklands"})
_MISSION_DESIGN_FOCUS = frozenset({"mission_design", "mission-design", "design"})


@dataclass(frozen=True)
class QagPage:
    id: str
    title: str
    html: str
    qag_era: str
    qag_types: tuple[str, ...]
    spec_mission_types: tuple[str, ...]
    theatres: tuple[str, ...]
    keywords: tuple[str, ...]
    enabled: bool
    skip_reason: str = ""
    snippet_extra: str = ""


class _QagHtmlExtractor(HTMLParser):
    """Pull title, lead copy, warn notes, and a few <code> labels from QAG HTML."""

    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self._in_title = False
        self._in_h1 = False
        self._in_p = False
        self._in_code = False
        self._in_note = False
        self._p_is_lead = False
        self._note_is_warn = False
        self._buf: list[str] = []
        self._code_buf: list[str] = []
        self.title = ""
        self.h1 = ""
        self.leads: list[str] = []
        self.warns: list[str] = []
        self.codes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"style", "script"}:
            self._skip += 1
            return
        if self._skip:
            return
        classes = set(((dict(attrs).get("class") or "") or "").split())
        if tag == "title":
            self._in_title = True
            self._buf = []
        elif tag == "h1":
            self._in_h1 = True
            self._buf = []
        elif tag == "p":
            self._in_p = True
            self._p_is_lead = "lead" in classes
            self._buf = []
        elif tag == "code":
            self._in_code = True
            self._code_buf = []
        elif tag == "div" and "note" in classes:
            self._in_note = True
            self._note_is_warn = "warn" in classes
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"style", "script"}:
            self._skip = max(0, self._skip - 1)
            return
        if self._skip:
            return
        text = " ".join("".join(self._buf).split()).strip()
        if tag == "title" and self._in_title:
            self.title = text
            self._in_title = False
        elif tag == "h1" and self._in_h1:
            self.h1 = text
            self._in_h1 = False
        elif tag == "p" and self._in_p:
            if text and (self._p_is_lead or len(self.leads) < _MAX_LEADS):
                self.leads.append(text)
            self._in_p = False
        elif tag == "code" and self._in_code:
            code = " ".join("".join(self._code_buf).split()).strip()
            if code and code not in self.codes and len(self.codes) < _MAX_CODE_LABELS:
                self.codes.append(code)
            self._in_code = False
        elif tag == "div" and self._in_note:
            if text and self._note_is_warn:
                self.warns.append(text)
            self._in_note = False

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        if self._in_code:
            self._code_buf.append(data)
        if self._in_title or self._in_h1 or self._in_p or self._in_note:
            self._buf.append(data)


def _as_tuple(value: Any) -> tuple[str, ...]:
    if not value:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(v) for v in value)


def _page_from_row(row: dict[str, Any]) -> QagPage:
    return QagPage(
        id=str(row.get("id") or "").strip(),
        title=str(row.get("title") or "").strip(),
        html=str(row.get("html") or "").strip().replace("\\", "/"),
        qag_era=str(row.get("qag_era") or "").strip(),
        qag_types=_as_tuple(row.get("qag_types")),
        spec_mission_types=tuple(s.lower() for s in _as_tuple(row.get("spec_mission_types"))),
        theatres=_as_tuple(row.get("theatres")),
        keywords=_as_tuple(row.get("keywords")),
        enabled=bool(row.get("enabled", True)),
        skip_reason=str(row.get("skip_reason") or "").strip(),
        snippet_extra=str(row.get("snippet_extra") or "").strip(),
    )


@lru_cache(maxsize=1)
def load_qag_index() -> tuple[QagPage, ...]:
    raw = (resources.files(_DATA_PKG) / _INDEX_NAME).read_text(encoding="utf-8")
    payload = yaml.safe_load(raw) or {}
    pages = [_page_from_row(row) for row in (payload.get("pages") or []) if isinstance(row, dict)]
    return tuple(p for p in pages if p.id)


def resolve_research_root(explicit: Path | str | None = None) -> Path | None:
    """Return the local gitignored ``research/`` dump, or None if absent."""
    if explicit is not None:
        path = Path(explicit)
        return path if path.is_dir() else None
    env = (os.environ.get(ENV_RESEARCH_DIR) or "").strip()
    if env:
        path = Path(env)
        return path if path.is_dir() else None
    start = Path.cwd().resolve()
    for candidate in (start, *start.parents):
        research = candidate / "research"
        if research.is_dir():
            return research
    return None


def _html_path(root: Path, page: QagPage) -> Path | None:
    rel = page.html.strip()
    if not rel:
        return None
    parts = Path(rel).parts
    if not parts or any(part in {os.pardir, os.curdir} for part in parts):
        return None
    path = (root / Path(*parts)).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path if path.is_file() else None


def _extract(path: Path) -> _QagHtmlExtractor:
    parser = _QagHtmlExtractor()
    try:
        blob = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return parser
    parser.feed(blob)
    return parser


def _note_for_page(page: QagPage, path: Path) -> dict[str, str]:
    extracted = _extract(path)
    title = extracted.h1 or extracted.title or page.title or page.id
    parts: list[str] = [QAG_DISCLAIMER]
    if page.snippet_extra:
        parts.append(page.snippet_extra)
    if page.qag_types:
        parts.append("QAG types: " + ", ".join(page.qag_types) + ".")
    if extracted.leads:
        parts.append(extracted.leads[0])
    if extracted.warns:
        parts.append(extracted.warns[0])
    if extracted.codes:
        parts.append("Example QAG labels (not Spec ids): " + ", ".join(extracted.codes) + ".")
    return {
        "title": title,
        "snippet": " ".join(parts),
        "source": f"fixture:qag:{page.id}",
    }


def score_qag_page(
    page: QagPage,
    *,
    query: str = "",
    mission_type: str | None = None,
    theatre: str | None = None,
    focus: str | None = None,
) -> int:
    if not page.enabled or not page.html:
        return 0
    score = 0
    q = (query or "").lower()
    focus_l = (focus or "").strip().lower()
    if focus_l in _MISSION_DESIGN_FOCUS:
        score += 2
    mt = (mission_type or "").strip().lower()
    if mt and mt in page.spec_mission_types:
        score += 4
    for kw in page.keywords:
        if kw.lower() and kw.lower() in q:
            score += 2
    for qag_type in page.qag_types:
        if qag_type.lower() in q:
            score += 3
    slug = page.id.replace("-", " ")
    if slug in q or (page.title and page.title.lower() in q):
        score += 2
    th = (theatre or "").strip().lower()
    if th:
        page_theatres = {t.lower() for t in page.theatres}
        if th in page_theatres or (page.qag_era == "wwii" and th in _WWII_THEATRES):
            score += 3
        elif page.qag_era.startswith("cold") and th in _MODERN_THEATRES:
            score += 2
        elif (page.qag_era == "wwii" and th in _MODERN_THEATRES) or (
            page.qag_era.startswith("cold") and th in _WWII_THEATRES
        ):
            score -= 1
    return score


def qag_fixture_notes(
    *,
    query: str = "",
    mission_type: str | None = None,
    theatre: str | None = None,
    focus: str | None = None,
    research_root: Path | str | None = None,
) -> list[dict[str, str]]:
    """Return matching QAG notes from local ``research/`` HTML, or [] if absent."""
    root = resolve_research_root(research_root)
    if root is None:
        return []
    ranked: list[tuple[int, QagPage, Path]] = []
    for page in load_qag_index():
        path = _html_path(root, page)
        if path is None:
            continue
        score = score_qag_page(
            page,
            query=query,
            mission_type=mission_type,
            theatre=theatre,
            focus=focus,
        )
        if score > 0:
            ranked.append((score, page, path))
    ranked.sort(key=lambda item: (-item[0], item[1].id))
    notes: list[dict[str, str]] = []
    for _score, page, path in ranked[:_MAX_QAG_NOTES]:
        notes.append(_note_for_page(page, path))
    return notes


def is_qag_fixture_source(source: str) -> bool:
    return (source or "").strip().lower().startswith("fixture:qag:")
