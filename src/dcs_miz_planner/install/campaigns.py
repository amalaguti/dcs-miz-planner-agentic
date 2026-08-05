"""Read-only index of installed DCS campaigns under Mods/campaigns.

Lists ``.cmp`` metadata, ``.miz`` filenames, and ``Doc/*.pdf`` filenames only —
does not extract PDF body text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .discover import discover_dcs_roots
from .models import Diagnostic

_NAME_EN_RE = re.compile(r'\["name_EN"\]\s*=\s*"((?:\\.|[^"\\])*)"', re.DOTALL)
_NAME_RE = re.compile(r'\["name"\]\s*=\s*"((?:\\.|[^"\\])*)"', re.DOTALL)
_DESC_RE = re.compile(r'\["description"\]\s*=\s*"((?:\\.|[^"\\])*)"', re.DOTALL)
_FILE_RE = re.compile(r'\["file"\]\s*=\s*"((?:\\.|[^"\\])*)"')


def _unescape_lua_string(raw: str) -> str:
    return raw.replace(r"\\", "\\").replace(r"\"", '"').replace(r"\n", "\n").replace(r"\t", "\t")


@dataclass(frozen=True)
class CampaignMissionRef:
    filename: str


@dataclass(frozen=True)
class CampaignDocRef:
    filename: str


@dataclass(frozen=True)
class CampaignSummary:
    name: str
    path: str
    description: str | None = None
    missions: tuple[CampaignMissionRef, ...] = ()
    docs: tuple[CampaignDocRef, ...] = ()
    cmp_file: str | None = None


@dataclass(frozen=True)
class CampaignIndex:
    dcs_roots: tuple[str, ...] = ()
    campaigns: tuple[CampaignSummary, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = field(default_factory=tuple)


def _parse_cmp_text(text: str) -> tuple[str | None, str | None, list[str]]:
    """Lightweight .cmp Lua-table scrape: display name, description, mission files."""
    name: str | None = None
    m = _NAME_EN_RE.search(text)
    if m:
        name = _unescape_lua_string(m.group(1)).strip() or None
    if not name:
        m = _NAME_RE.search(text)
        if m:
            name = _unescape_lua_string(m.group(1)).strip() or None

    description: str | None = None
    d = _DESC_RE.search(text)
    if d:
        description = _unescape_lua_string(d.group(1)).strip() or None
        if description and len(description) > 500:
            description = description[:497] + "..."

    files: list[str] = []
    seen: set[str] = set()
    for fm in _FILE_RE.finditer(text):
        fname = _unescape_lua_string(fm.group(1)).strip()
        if fname and fname.lower().endswith(".miz") and fname not in seen:
            seen.add(fname)
            files.append(fname)
    return name, description, files


def scan_campaigns_root(campaigns_dir: Path) -> list[CampaignSummary]:
    """Scan one ``Mods/campaigns`` directory; no `.miz` unzip."""
    if not campaigns_dir.is_dir():
        return []

    summaries: list[CampaignSummary] = []
    for child in sorted(campaigns_dir.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir():
            continue
        cmp_paths = sorted(child.glob("*.cmp"))
        cmp_file = cmp_paths[0].name if cmp_paths else None
        name: str | None = None
        description: str | None = None
        cmp_missions: list[str] = []
        if cmp_paths:
            try:
                text = cmp_paths[0].read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            name, description, cmp_missions = _parse_cmp_text(text)

        disk_miz = sorted(p.name for p in child.glob("*.miz"))
        mission_names = cmp_missions or disk_miz
        # Prefer union when both present (cmp order first, then extras on disk).
        if cmp_missions and disk_miz:
            seen = set(cmp_missions)
            mission_names = list(cmp_missions) + [m for m in disk_miz if m not in seen]

        doc_dir = child / "Doc"
        docs: list[CampaignDocRef] = []
        if doc_dir.is_dir():
            for pdf in sorted(doc_dir.glob("*.pdf"), key=lambda p: p.name.lower()):
                docs.append(CampaignDocRef(filename=pdf.name))

        if not mission_names and not docs and not cmp_file:
            continue

        summaries.append(
            CampaignSummary(
                name=name or child.name,
                path=str(child.resolve()),
                description=description,
                missions=tuple(CampaignMissionRef(filename=m) for m in mission_names),
                docs=tuple(docs),
                cmp_file=cmp_file,
            )
        )
    return summaries


def index_installed_campaigns(
    *,
    explicit_root: Path | str | None = None,
    env: dict[str, str] | None = None,
    campaigns_dir: Path | str | None = None,
) -> CampaignIndex:
    """
    Discover DCS roots and list campaigns under ``Mods/campaigns``.

    Doc entries are PDF filenames only (no text extract). ``campaigns_dir`` overrides
    discovery for hermetic tests (points at a fake campaigns tree directly).
    """
    diagnostics: list[Diagnostic] = []

    if campaigns_dir is not None:
        # Hermetic override: ``campaigns_dir`` is the campaigns folder itself
        # (children are individual campaign packs).
        camps = scan_campaigns_root(Path(campaigns_dir))
        return CampaignIndex(
            dcs_roots=(),
            campaigns=tuple(camps),
            diagnostics=tuple(diagnostics),
        )

    roots, disc_diags = discover_dcs_roots(explicit=explicit_root, env=env)
    diagnostics.extend(disc_diags)
    if not roots:
        return CampaignIndex(diagnostics=tuple(diagnostics))

    all_camps: list[CampaignSummary] = []
    seen_paths: set[str] = set()
    for dcs_root in roots:
        camp_root = dcs_root / "Mods" / "campaigns"
        if not camp_root.is_dir():
            diagnostics.append(
                Diagnostic(f"No Mods/campaigns under DCS root: {dcs_root}", str(dcs_root))
            )
            continue
        for summary in scan_campaigns_root(camp_root):
            if summary.path in seen_paths:
                continue
            seen_paths.add(summary.path)
            all_camps.append(summary)

    return CampaignIndex(
        dcs_roots=tuple(str(r.resolve()) for r in roots),
        campaigns=tuple(all_camps),
        diagnostics=tuple(diagnostics),
    )
