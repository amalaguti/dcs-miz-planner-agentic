"""Soft-check known Channel aircraft packs against a local DCS install.

Does not harvest modules into registry YAML (#8a.1). Folder presence only.
"""

from __future__ import annotations

from pathlib import Path

from ..models import MissionSpec

# Spec aircraft id → relative folders under a DCS root (any one present = installed).
# FW-190 Spec ids omit hyphens; ED folders use them under CoreMods/WWII Units.
_AIRCRAFT_FOLDERS: dict[str, tuple[str, ...]] = {
    "SpitfireLFMkIX": (
        "Mods/aircraft/SpitfireLFMkIX",
        "CoreMods/WWII Units/SpitfireLFMkIX",
    ),
    "SpitfireLFMkIXCW": (
        "Mods/aircraft/SpitfireLFMkIX",
        "CoreMods/WWII Units/SpitfireLFMkIX",
    ),
    "MosquitoFBMkVI": ("CoreMods/WWII Units/MosquitoFBMkVI",),
    "Bf-109K-4": ("CoreMods/WWII Units/Bf-109K-4",),
    "FW-190A8": ("CoreMods/WWII Units/FW-190A-8",),
    "FW-190D9": ("CoreMods/WWII Units/FW-190D-9",),
}


def aircraft_folder_candidates(aircraft_id: str) -> tuple[str, ...]:
    return _AIRCRAFT_FOLDERS.get(aircraft_id, ())


def aircraft_module_present(dcs_root: Path, aircraft_id: str) -> bool:
    """True if any mapped folder exists under ``dcs_root``."""
    for rel in aircraft_folder_candidates(aircraft_id):
        if (dcs_root / rel).is_dir():
            return True
    return False


def existing_dcs_roots(dcs_roots: tuple[str, ...] | list[str]) -> list[Path]:
    roots: list[Path] = []
    for raw in dcs_roots:
        path = Path(raw)
        if path.is_dir():
            roots.append(path)
    return roots


def spec_aircraft_refs(spec: MissionSpec) -> list[tuple[str, str]]:
    """Return (path, aircraft_id) for player, enemies, and package flights."""
    refs: list[tuple[str, str]] = [("player.aircraft", spec.player.aircraft)]
    for i, enemy in enumerate(spec.enemies):
        refs.append((f"enemies[{i}].aircraft", enemy.aircraft))
    for i, flight in enumerate(spec.package):
        refs.append((f"package[{i}].aircraft", flight.aircraft))
    return refs


def missing_aircraft_module_messages(
    spec: MissionSpec,
    dcs_roots: tuple[str, ...] | list[str],
) -> list[tuple[str, str, str]]:
    """
    Return list of (path, aircraft_id, message) for missing known modules.

    Empty when no roots exist on disk or every referenced known aircraft is present
    on at least one root.
    """
    roots = existing_dcs_roots(dcs_roots)
    if not roots:
        return []

    missing: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for path, aircraft_id in spec_aircraft_refs(spec):
        if aircraft_id in seen:
            continue
        candidates = aircraft_folder_candidates(aircraft_id)
        if not candidates:
            continue
        if any(aircraft_module_present(root, aircraft_id) for root in roots):
            seen.add(aircraft_id)
            continue
        seen.add(aircraft_id)
        missing.append(
            (
                path,
                aircraft_id,
                (
                    f"Aircraft module for '{aircraft_id}' was not found under the local "
                    f"DCS install (checked Mods/aircraft and CoreMods/WWII Units). "
                    f"The Spec is still valid; DCS may fail to load this aircraft."
                ),
            )
        )
    return missing
