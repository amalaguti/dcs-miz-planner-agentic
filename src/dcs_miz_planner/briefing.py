"""Mission briefing texts for DCS ``l10n`` dictionary (compile-time).

Derived from the squadron-commander brief builder — deterministic Spec → plain text,
never LLM-authored Lua.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Coalition, MissionSpec

_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_HEADING_LINE_RE = re.compile(r"^#+\s*")


@dataclass(frozen=True)
class MissionBriefingTexts:
    """Plain-text strings for PyDCS briefing setters."""

    sortie: str
    description: str
    blue_task: str
    red_task: str


def _plain(text: str) -> str:
    """Strip markdown heading markers; collapse excess blank lines."""
    lines: list[str] = []
    for line in text.splitlines():
        stripped = _HEADING_LINE_RE.sub("", line).rstrip()
        lines.append(stripped)
    # Trim leading/trailing empties; keep single blank between blocks.
    out: list[str] = []
    prev_blank = True
    for line in lines:
        blank = not line.strip()
        if blank and prev_blank:
            continue
        out.append(line.rstrip())
        prev_blank = blank
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out).strip()


def _parse_sections(brief: str) -> dict[str, str]:
    """Map lowercased section titles to body text (from ``## Title`` markers)."""
    matches = list(_SECTION_RE.finditer(brief))
    sections: dict[str, str] = {}
    for i, match in enumerate(matches):
        title = match.group(1).strip().lower()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(brief)
        body = brief[start:end].strip()
        sections[title] = body
    return sections


def _section(sections: dict[str, str], *needles: str) -> str:
    for key, body in sections.items():
        for needle in needles:
            if needle in key:
                return body.strip()
    return ""


def _split_watch_and_closing(watch_block: str) -> tuple[str, str]:
    """Last non-empty paragraph after Watch-outs is the closing line."""
    parts = [p.strip() for p in re.split(r"\n\s*\n", watch_block.strip()) if p.strip()]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return "\n\n".join(parts[:-1]), parts[-1]


def build_mission_briefing_texts(
    spec: MissionSpec,
    voice: str | None = None,
) -> MissionBriefingTexts:
    """Build Sortie / Description / Blue / Red task strings for ``.miz`` l10n."""
    # Lazy import: avoid compiler ↔ agent ↔ tools circular import at package load.
    from .agent.voice import DEFAULT_VOICE, build_commander_brief, normalize_voice

    resolved = normalize_voice(voice) if voice else None
    resolved = resolved or DEFAULT_VOICE
    brief = build_commander_brief(spec, resolved)
    sections = _parse_sections(brief)

    situation = _section(sections, "situation", "sortie")
    tactics = _section(sections, "tactics")
    procedures = _section(sections, "procedures")
    watch_raw = _section(sections, "watch")
    watch, closing = _split_watch_and_closing(watch_raw)

    desc_parts: list[str] = []
    if spec.description.strip():
        desc_parts.append(spec.description.strip())
    if situation:
        desc_parts.append(situation)
    if watch:
        desc_parts.append(watch)
    description = _plain("\n\n".join(desc_parts))

    task_parts = [p for p in (tactics, procedures, closing) if p]
    player_task = _plain("\n\n".join(task_parts))

    blue_task = ""
    red_task = ""
    if spec.player.coalition is Coalition.BLUE:
        blue_task = player_task
    else:
        red_task = player_task

    return MissionBriefingTexts(
        sortie=_plain(spec.name) or "Mission",
        description=description or _plain(situation) or spec.name,
        blue_task=blue_task,
        red_task=red_task,
    )
