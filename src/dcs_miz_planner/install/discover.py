"""Locate DCS install roots and Saved Games profiles."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .models import Diagnostic

ENV_DCS_ROOT = "DCS_MIZ_DCS_ROOT"
ENV_SAVED_GAMES = "DCS_MIZ_SAVED_GAMES"

_REGISTRY_SUBKEYS = (
    r"SOFTWARE\Eagle Dynamics\DCS World",
    r"SOFTWARE\Eagle Dynamics\DCS World OpenBeta",
    r"SOFTWARE\WOW6432Node\Eagle Dynamics\DCS World",
    r"SOFTWARE\WOW6432Node\Eagle Dynamics\DCS World OpenBeta",
)


def _is_dcs_root(path: Path) -> bool:
    return (path / "autoupdate.cfg").is_file() or (path / "Mods" / "terrains").is_dir()


def _registry_dcs_paths() -> list[Path]:
    """Read install Path values written by the DCS installer (Windows only)."""
    if sys.platform != "win32":
        return []
    try:
        import winreg
    except ImportError:  # pragma: no cover
        return []

    found: list[Path] = []
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for subkey in _REGISTRY_SUBKEYS:
            try:
                with winreg.OpenKey(hive, subkey) as key:
                    value, _ = winreg.QueryValueEx(key, "Path")
            except OSError:
                continue
            if isinstance(value, str) and value.strip():
                found.append(Path(value.strip()))
    return found


def discover_dcs_roots(
    *,
    explicit: Path | str | None = None,
    env: dict[str, str] | None = None,
) -> tuple[list[Path], list[Diagnostic]]:
    """Return distinct DCS install roots; never silently merges variants."""
    env = env if env is not None else os.environ
    diagnostics: list[Diagnostic] = []

    if explicit is not None:
        root = Path(explicit).expanduser().resolve()
        if not root.is_dir():
            return [], [
                Diagnostic(f"DCS root does not exist or is not a directory: {root}", str(root))
            ]
        if not _is_dcs_root(root):
            return [], [
                Diagnostic(
                    "Path does not look like a DCS install "
                    "(missing autoupdate.cfg and Mods/terrains): "
                    f"{root}",
                    str(root),
                )
            ]
        return [root], diagnostics

    env_root = env.get(ENV_DCS_ROOT)
    if env_root:
        return discover_dcs_roots(explicit=env_root, env=env)

    candidates: list[Path] = []
    # Always consult the registry helper so tests can monkeypatch it on any OS.
    # The real implementation returns [] on non-Windows.
    candidates.extend(_registry_dcs_paths())
    if sys.platform == "win32":
        for key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            base = env.get(key)
            if not base:
                continue
            base_path = Path(base)
            for name in (
                "Eagle Dynamics/DCS World",
                "Eagle Dynamics/DCS World OpenBeta",
                "DCS World",
                "DCS World OpenBeta",
            ):
                candidates.append(base_path / name)
        steam = env.get("ProgramFiles(x86)")
        if steam:
            candidates.append(Path(steam) / "Steam/steamapps/common/DCS World")

    found: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            resolved = candidate.expanduser().resolve()
        except OSError:
            continue
        key = str(resolved).lower()
        if key in seen:
            continue
        if resolved.is_dir() and _is_dcs_root(resolved):
            seen.add(key)
            found.append(resolved)

    if not found:
        diagnostics.append(
            Diagnostic(f"No DCS installation found. Pass --dcs-root or set {ENV_DCS_ROOT}.")
        )
    elif len(found) > 1:
        diagnostics.append(
            Diagnostic(
                "Multiple DCS installations found; reporting all without merging: "
                + ", ".join(str(p) for p in found)
            )
        )
    return found, diagnostics


def discover_saved_games_roots(
    *,
    explicit: Path | str | None = None,
    env: dict[str, str] | None = None,
) -> tuple[list[Path], list[Diagnostic]]:
    """Return Saved Games DCS* profile directories."""
    env = env if env is not None else os.environ
    diagnostics: list[Diagnostic] = []

    if explicit is not None:
        root = Path(explicit).expanduser().resolve()
        if not root.is_dir():
            return [], [
                Diagnostic(
                    f"Saved Games root does not exist or is not a directory: {root}",
                    str(root),
                )
            ]
        return [root], diagnostics

    env_root = env.get(ENV_SAVED_GAMES)
    if env_root:
        return discover_saved_games_roots(explicit=env_root, env=env)

    home = Path.home()
    user_profile = env.get("USERPROFILE")
    bases = [home]
    if user_profile:
        bases.append(Path(user_profile))

    found: list[Path] = []
    seen: set[str] = set()
    for base in bases:
        saved = base / "Saved Games"
        if not saved.is_dir():
            continue
        for child in sorted(saved.iterdir()):
            if not child.is_dir():
                continue
            name = child.name
            if name == "DCS" or name.startswith("DCS."):
                key = str(child.resolve()).lower()
                if key in seen:
                    continue
                seen.add(key)
                found.append(child.resolve())

    if not found:
        diagnostics.append(
            Diagnostic(
                "No Saved Games DCS profile found; enable/disable overrides will be ignored. "
                f"Pass --saved-games or set {ENV_SAVED_GAMES}."
            )
        )
    return found, diagnostics
