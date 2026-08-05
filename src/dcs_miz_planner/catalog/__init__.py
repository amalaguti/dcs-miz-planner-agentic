"""Agent-facing known catalog (SQLite), synced from Channel YAML + Spec enums."""

from __future__ import annotations

from ..install.store import default_db_path
from .models import (
    AircraftAvailabilityView,
    CatalogAircraft,
    CatalogAirfield,
    CatalogEnumRow,
    CatalogPayload,
    CatalogPlanningOption,
    CatalogSnapshot,
    CatalogTheatre,
    CatalogWeatherPreset,
    TheatreAvailabilityView,
)
from .service import (
    LIST_TYPES,
    CatalogService,
    join_aircraft_views,
    join_theatre_views,
)
from .store import CATALOG_SCHEMA_VERSION, CatalogStore
from .sync import SOURCE_LABEL, build_snapshot_from_registry

__all__ = [
    "CATALOG_SCHEMA_VERSION",
    "LIST_TYPES",
    "SOURCE_LABEL",
    "AircraftAvailabilityView",
    "CatalogAircraft",
    "CatalogAirfield",
    "CatalogEnumRow",
    "CatalogPayload",
    "CatalogPlanningOption",
    "CatalogService",
    "CatalogSnapshot",
    "CatalogStore",
    "CatalogTheatre",
    "CatalogWeatherPreset",
    "TheatreAvailabilityView",
    "build_snapshot_from_registry",
    "default_db_path",
    "join_aircraft_views",
    "join_theatre_views",
]
