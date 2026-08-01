"""Typed rows for the known agent catalog and theatre discovery views."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CatalogTheatre:
    theatre_id: str


@dataclass(frozen=True)
class CatalogAirfield:
    name: str
    airdrome_id: int
    theatre_id: str


@dataclass(frozen=True)
class CatalogAircraft:
    aircraft_id: str
    radio_mhz: float


@dataclass(frozen=True)
class CatalogWeatherPreset:
    name: str
    description: str


@dataclass(frozen=True)
class CatalogPayload:
    name: str
    meta_json: str


@dataclass(frozen=True)
class CatalogPlanningOption:
    family: str
    id: str
    label: str
    description: str
    support: str
    meta_json: str


@dataclass(frozen=True)
class CatalogEnumRow:
    value: str


@dataclass(frozen=True)
class TheatreAvailabilityView:
    """Known catalog theatre joined with local install discovery."""

    theatre_id: str
    known: bool
    installed: bool
    install_state: str | None
    planner_supported: bool
    offerable: bool
    dcs_root: str | None = None


@dataclass(frozen=True)
class CatalogSnapshot:
    """In-memory known catalog after sync or load."""

    synced_at: datetime
    source: str
    theatres: tuple[CatalogTheatre, ...]
    airfields: tuple[CatalogAirfield, ...]
    aircraft: tuple[CatalogAircraft, ...]
    weather_presets: tuple[CatalogWeatherPreset, ...]
    payloads: tuple[CatalogPayload, ...]
    planning_options: tuple[CatalogPlanningOption, ...]
    mission_types: tuple[CatalogEnumRow, ...]
    start_types: tuple[CatalogEnumRow, ...]
    coalitions: tuple[CatalogEnumRow, ...]
    objective_types: tuple[CatalogEnumRow, ...]
    countries: tuple[CatalogEnumRow, ...]
