"""Agent-facing known catalog (SQLite), synced from Channel YAML + Spec enums."""

from __future__ import annotations

from ..install.store import default_db_path
from .models import (
    CatalogAircraft,
    CatalogAirfield,
    CatalogEnumRow,
    CatalogPayload,
    CatalogSnapshot,
    CatalogTheatre,
    CatalogWeatherPreset,
    TheatreAvailabilityView,
)
from .service import (
    AIRCRAFT_DISCOVERY_DEFERRED,
    LIST_TYPES,
    CatalogService,
    join_theatre_views,
)
from .store import CATALOG_SCHEMA_VERSION, CatalogStore
from .sync import SOURCE_LABEL, build_snapshot_from_registry

__all__ = [
    "AIRCRAFT_DISCOVERY_DEFERRED",
    "CATALOG_SCHEMA_VERSION",
    "LIST_TYPES",
    "SOURCE_LABEL",
    "CatalogAircraft",
    "CatalogAirfield",
    "CatalogEnumRow",
    "CatalogPayload",
    "CatalogService",
    "CatalogSnapshot",
    "CatalogStore",
    "CatalogTheatre",
    "CatalogWeatherPreset",
    "TheatreAvailabilityView",
    "build_snapshot_from_registry",
    "default_db_path",
    "join_theatre_views",
]
