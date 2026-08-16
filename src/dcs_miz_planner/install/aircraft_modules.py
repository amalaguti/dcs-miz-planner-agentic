"""Aircraft module folder presence and install harvest (discovery-only).

Soft-warn (#38) maps Spec ids → folders. Harvest (#8a.1) lists folders into
inventory cache — never into registry YAML.
"""

from __future__ import annotations

from pathlib import Path

from ..models import MissionSpec
from .models import AircraftModuleRecord

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
    "Su-25T": ("CoreMods/aircraft/Su-25T",),
}

# Shared asset dirs under CoreMods/WWII Units — not aircraft modules.
_WWII_UNITS_SKIP = frozenset(
    {
        "Encyclopedia",
        "ImagesGUI",
        "Options",
        "Theme",
        "UnitPayloads",
        "Weapons",
        "l10n",
    }
)

_SCAN_SPECS: tuple[tuple[str, bool], ...] = (
    ("Mods/aircraft", True),  # require entry.lua
    ("CoreMods/WWII Units", False),  # skip-list only (often no entry.lua)
    ("CoreMods/aircraft", True),  # require entry.lua
)


def aircraft_folder_candidates(aircraft_id: str) -> tuple[str, ...]:
    return _AIRCRAFT_FOLDERS.get(aircraft_id, ())


def known_ids_for_folder(source: str, folder_name: str) -> tuple[str, ...]:
    """Return Spec aircraft ids that map to ``source/folder_name``."""
    rel = f"{source}/{folder_name}".replace("\\", "/")
    ids = [aid for aid, folders in _AIRCRAFT_FOLDERS.items() if rel in folders]
    return tuple(sorted(ids))


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


def harvest_aircraft_modules(
    dcs_roots: list[Path] | tuple[Path, ...],
) -> list[AircraftModuleRecord]:
    """List aircraft-like module folders under each DCS root (no YAML writes)."""
    records: list[AircraftModuleRecord] = []
    for root in dcs_roots:
        for source, require_entry in _SCAN_SPECS:
            base = root / Path(source)
            if not base.is_dir():
                continue
            for child in sorted(base.iterdir(), key=lambda p: p.name.lower()):
                if not child.is_dir():
                    continue
                if source == "CoreMods/WWII Units" and child.name in _WWII_UNITS_SKIP:
                    continue
                if require_entry and not (child / "entry.lua").is_file():
                    continue
                known_ids = known_ids_for_folder(source, child.name)
                records.append(
                    AircraftModuleRecord(
                        folder_name=child.name,
                        dcs_root=str(root),
                        source=source,
                        folder_path=str(child),
                        known_aircraft_ids=known_ids,
                        planner_supported=bool(known_ids),
                        evidence=(f"dir:{child}",),
                    )
                )
    return records


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
