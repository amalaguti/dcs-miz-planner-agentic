"""Typed records for local DCS theatre availability."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AvailabilityState(str, Enum):
    AVAILABLE = "available"
    DISABLED = "disabled"
    INCOMPLETE = "incomplete"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Diagnostic:
    """Human-readable probe note tied to a source path when known."""

    message: str
    source: str | None = None


@dataclass(frozen=True)
class TheatreRecord:
    """One theatre observed (or partially observed) in a local DCS install."""

    theatre_id: str
    update_id: str | None
    dcs_root: str
    state: AvailabilityState
    planner_supported: bool
    terrain_path: str | None = None
    saved_games_root: str | None = None
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class AircraftModuleRecord:
    """One aircraft (or aircraft-like) module folder observed under a DCS root."""

    folder_name: str
    dcs_root: str
    source: str
    folder_path: str
    known_aircraft_ids: tuple[str, ...] = ()
    planner_supported: bool = False
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class TheatreInventory:
    """Cached or freshly scanned local theatre (+ aircraft module) inventory."""

    scanned_at: datetime
    dcs_roots: tuple[str, ...]
    saved_games_roots: tuple[str, ...]
    theatres: tuple[TheatreRecord, ...]
    aircraft_modules: tuple[AircraftModuleRecord, ...] = ()
    diagnostics: tuple[Diagnostic, ...] = ()
    from_cache: bool = False

    def available(self) -> list[TheatreRecord]:
        return [t for t in self.theatres if t.state is AvailabilityState.AVAILABLE]

    def available_and_supported(self) -> list[TheatreRecord]:
        return [t for t in self.available() if t.planner_supported]
