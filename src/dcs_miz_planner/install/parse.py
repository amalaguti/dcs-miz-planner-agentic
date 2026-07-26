"""Constrained readers for DCS install metadata — never execute Lua."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .models import Diagnostic

# Quoted string assignment: ['id'] = "TheChannel" or ["id"] = "TheChannel"
_QUOTED_FIELD = re.compile(
    r"""\[['\"](?P<key>id|update_id|state)['\"]\]\s*=\s*['\"](?P<value>[^'\"]+)['\"]""",
    re.IGNORECASE,
)
# local self_ID = "TheChannel";
_SELF_ID = re.compile(
    r"""local\s+self_ID\s*=\s*['\"](?P<value>[^'\"]+)['\"]""",
    re.IGNORECASE,
)
# pluginsEnabled = { ["MarianaIslands"] = false, ... }
_PLUGIN_BOOL = re.compile(
    r"""\[['\"](?P<key>[^'\"]+)['\"]\]\s*=\s*(?P<value>true|false)""",
    re.IGNORECASE,
)


def parse_autoupdate_modules(path: Path) -> tuple[set[str], list[Diagnostic]]:
    """Return updater module ids from autoupdate.cfg JSON."""
    diagnostics: list[Diagnostic] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return set(), [Diagnostic(f"Cannot read autoupdate.cfg: {exc}", str(path))]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return set(), [Diagnostic(f"Malformed autoupdate.cfg JSON: {exc}", str(path))]

    modules = data.get("modules")
    if not isinstance(modules, list):
        return set(), [Diagnostic("autoupdate.cfg missing modules list", str(path))]

    return {str(m) for m in modules if isinstance(m, (str, int))}, diagnostics


def parse_terrain_entry(path: Path) -> tuple[dict[str, str], list[Diagnostic]]:
    """Extract static id / update_id / state / plugin id from entry.lua as text."""
    diagnostics: list[Diagnostic] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {}, [Diagnostic(f"Cannot read terrain entry.lua: {exc}", str(path))]

    fields: dict[str, str] = {}
    for match in _QUOTED_FIELD.finditer(text):
        fields[match.group("key")] = match.group("value")

    self_id = _SELF_ID.search(text)
    if self_id:
        fields.setdefault("plugin_id", self_id.group("value"))
        fields.setdefault("id", self_id.group("value"))

    if "id" not in fields and "update_id" not in fields:
        diagnostics.append(
            Diagnostic("No extractable theatre id or update_id in entry.lua", str(path))
        )
    return fields, diagnostics


def parse_plugins_enabled(path: Path) -> tuple[dict[str, bool], list[Diagnostic]]:
    """Parse exact string→bool overrides from pluginsEnabled.lua without executing it."""
    diagnostics: list[Diagnostic] = []
    if not path.is_file():
        return {}, diagnostics
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {}, [Diagnostic(f"Cannot read pluginsEnabled.lua: {exc}", str(path))]

    overrides: dict[str, bool] = {}
    for match in _PLUGIN_BOOL.finditer(text):
        overrides[match.group("key")] = match.group("value").lower() == "true"
    return overrides, diagnostics
