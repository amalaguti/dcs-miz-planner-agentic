"""Public catalog API: sync known rows; join theatres/aircraft with install inventory."""

from __future__ import annotations

import json
from pathlib import Path

from ..install.models import (
    AircraftModuleRecord,
    AvailabilityState,
    TheatreInventory,
    TheatreRecord,
)
from ..install.service import InventoryService
from ..install.store import default_db_path
from ..registry import ChannelRegistry
from .models import AircraftAvailabilityView, CatalogSnapshot, TheatreAvailabilityView
from .store import CatalogStore
from .sync import build_snapshot_from_registry

LIST_TYPES = (
    "theatres",
    "airfields",
    "aircraft",
    "weather",
    "payloads",
    "planning_options",
    "strike_units",
    "mission_types",
    "start_types",
    "coalitions",
    "objective_types",
    "countries",
)

_VALID_OPTION_SUPPORT = frozenset({"supported", "advisory", "future"})


def _prefer_theatre(a: TheatreRecord, b: TheatreRecord) -> TheatreRecord:
    """Prefer available+supported rows when the same theatre appears under multiple roots."""

    def score(t: TheatreRecord) -> tuple[int, int]:
        available = 1 if t.state is AvailabilityState.AVAILABLE else 0
        supported = 1 if t.planner_supported else 0
        return (available, supported)

    return a if score(a) >= score(b) else b


def _prefer_aircraft_module(
    a: AircraftModuleRecord, b: AircraftModuleRecord
) -> AircraftModuleRecord:
    """Prefer planner-supported / Mods/aircraft when the same folder appears twice."""

    def score(m: AircraftModuleRecord) -> tuple[int, int]:
        supported = 1 if m.planner_supported else 0
        preferred_source = 1 if m.source == "Mods/aircraft" else 0
        return (supported, preferred_source)

    return a if score(a) >= score(b) else b


def join_theatre_views(
    known_ids: frozenset[str] | set[str],
    inventory: TheatreInventory | None,
) -> list[TheatreAvailabilityView]:
    """Merge known catalog theatres with install discovery (discovered-only included)."""
    by_id: dict[str, TheatreRecord] = {}
    if inventory is not None:
        for rec in inventory.theatres:
            existing = by_id.get(rec.theatre_id)
            by_id[rec.theatre_id] = rec if existing is None else _prefer_theatre(existing, rec)

    views: list[TheatreAvailabilityView] = []
    for theatre_id in sorted(set(known_ids) | set(by_id)):
        known = theatre_id in known_ids
        rec = by_id.get(theatre_id)
        installed = rec is not None
        state = rec.state.value if rec is not None else None
        planner = bool(rec.planner_supported) if rec is not None else False
        offerable = (
            known
            and rec is not None
            and rec.state is AvailabilityState.AVAILABLE
            and rec.planner_supported
        )
        views.append(
            TheatreAvailabilityView(
                theatre_id=theatre_id,
                known=known,
                installed=installed,
                install_state=state,
                planner_supported=planner,
                offerable=offerable,
                dcs_root=rec.dcs_root if rec is not None else None,
            )
        )
    return views


def join_aircraft_views(
    known_ids: frozenset[str] | set[str],
    inventory: TheatreInventory | None,
) -> list[AircraftAvailabilityView]:
    """Merge known catalog aircraft with install module discovery."""
    by_known_id: dict[str, AircraftModuleRecord] = {}
    discovered_only: dict[tuple[str, str], AircraftModuleRecord] = {}

    if inventory is not None:
        for rec in inventory.aircraft_modules:
            if rec.known_aircraft_ids:
                for aid in rec.known_aircraft_ids:
                    existing = by_known_id.get(aid)
                    by_known_id[aid] = (
                        rec if existing is None else _prefer_aircraft_module(existing, rec)
                    )
            else:
                key = (rec.folder_name, rec.source)
                existing = discovered_only.get(key)
                discovered_only[key] = (
                    rec if existing is None else _prefer_aircraft_module(existing, rec)
                )

    views: list[AircraftAvailabilityView] = []
    for aircraft_id in sorted(set(known_ids) | set(by_known_id)):
        known = aircraft_id in known_ids
        rec = by_known_id.get(aircraft_id)
        installed = rec is not None
        planner = known
        offerable = known and installed
        views.append(
            AircraftAvailabilityView(
                aircraft_id=aircraft_id,
                known=known,
                installed=installed,
                planner_supported=planner,
                offerable=offerable,
                source=rec.source if rec is not None else None,
                dcs_root=rec.dcs_root if rec is not None else None,
                folder_name=rec.folder_name if rec is not None else None,
            )
        )

    for rec in sorted(discovered_only.values(), key=lambda m: (m.folder_name, m.source)):
        views.append(
            AircraftAvailabilityView(
                aircraft_id=rec.folder_name,
                known=False,
                installed=True,
                planner_supported=False,
                offerable=False,
                source=rec.source,
                dcs_root=rec.dcs_root,
                folder_name=rec.folder_name,
            )
        )
    return views


class CatalogService:
    """SQLite-backed known catalog with optional install join for theatres/aircraft."""

    def __init__(
        self,
        *,
        db_path: Path | str | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.db_path = Path(db_path) if db_path else default_db_path(env=env)
        self.env = env
        self._store = CatalogStore(self.db_path)

    def sync(self, registry: ChannelRegistry | None = None) -> CatalogSnapshot:
        snapshot = build_snapshot_from_registry(registry)
        self._store.replace_snapshot(snapshot)
        loaded = self._store.load_snapshot()
        if loaded is None:  # pragma: no cover - replace just wrote
            return snapshot
        return loaded

    def get_snapshot(self) -> CatalogSnapshot | None:
        return self._store.load_snapshot()

    def ensure_synced(self, registry: ChannelRegistry | None = None) -> CatalogSnapshot:
        existing = self.get_snapshot()
        if existing is not None:
            return existing
        return self.sync(registry)

    def list_theatres(
        self,
        *,
        inventory: TheatreInventory | None = None,
        include_discovered: bool = True,
    ) -> list[TheatreAvailabilityView]:
        snap = self.ensure_synced()
        known = frozenset(t.theatre_id for t in snap.theatres)
        if inventory is None and include_discovered:
            inv_svc = InventoryService(db_path=self.db_path, env=self.env)
            inventory = inv_svc.get() if inv_svc.has_cache() else None
        views = join_theatre_views(known, inventory if include_discovered else None)
        if not include_discovered:
            return [v for v in views if v.known]
        return views

    def list_aircraft(
        self,
        *,
        inventory: TheatreInventory | None = None,
        include_discovered: bool = True,
    ) -> list[AircraftAvailabilityView]:
        snap = self.ensure_synced()
        known = frozenset(a.aircraft_id for a in snap.aircraft)
        if inventory is None and include_discovered:
            inv_svc = InventoryService(db_path=self.db_path, env=self.env)
            inventory = inv_svc.get() if inv_svc.has_cache() else None
        views = join_aircraft_views(known, inventory if include_discovered else None)
        if not include_discovered:
            return [v for v in views if v.known]
        return views

    def list_rows(
        self,
        resource_type: str,
        *,
        family: str | None = None,
        support: str | None = None,
    ) -> list[dict[str, object]]:
        """Return known catalog rows as plain dicts for CLI/JSON (not theatres join)."""
        if resource_type not in LIST_TYPES:
            raise ValueError(
                f"Unknown catalog type {resource_type!r}. Known: {', '.join(LIST_TYPES)}"
            )
        snap = self.ensure_synced()
        if resource_type == "theatres":
            return [{"theatre_id": t.theatre_id, "known": True} for t in snap.theatres]
        if resource_type == "airfields":
            return [
                {
                    "name": a.name,
                    "airdrome_id": a.airdrome_id,
                    "theatre_id": a.theatre_id,
                }
                for a in snap.airfields
            ]
        if resource_type == "aircraft":
            return [{"aircraft_id": a.aircraft_id, "radio_mhz": a.radio_mhz} for a in snap.aircraft]
        if resource_type == "weather":
            return [{"name": w.name, "description": w.description} for w in snap.weather_presets]
        if resource_type == "payloads":
            return [{"name": p.name, "meta_json": p.meta_json} for p in snap.payloads]
        if resource_type == "planning_options":
            if support is not None and support not in _VALID_OPTION_SUPPORT:
                raise ValueError(
                    f"Unknown support {support!r}. Known: {', '.join(sorted(_VALID_OPTION_SUPPORT))}"
                )
            rows: list[dict[str, object]] = []
            for opt in snap.planning_options:
                if family is not None and opt.family != family:
                    continue
                if support is not None and opt.support != support:
                    continue
                rows.append(
                    {
                        "family": opt.family,
                        "id": opt.id,
                        "label": opt.label,
                        "description": opt.description,
                        "support": opt.support,
                        "meta_json": opt.meta_json,
                    }
                )
            return rows
        if resource_type == "strike_units":
            out: list[dict[str, object]] = []
            for u in snap.strike_units:
                try:
                    class_ids = json.loads(u.class_ids_json) if u.class_ids_json else []
                except json.JSONDecodeError:
                    class_ids = []
                if not isinstance(class_ids, list):
                    class_ids = []
                out.append(
                    {
                        "unit_id": u.unit_id,
                        "label": u.label,
                        "domain": u.domain,
                        "theatre_id": u.theatre_id,
                        "era_id": u.era_id,
                        "class_ids": [str(c) for c in class_ids],
                        "class_ids_json": u.class_ids_json,
                    }
                )
            return out
        enum_map = {
            "mission_types": snap.mission_types,
            "start_types": snap.start_types,
            "coalitions": snap.coalitions,
            "objective_types": snap.objective_types,
            "countries": snap.countries,
        }
        return [{"value": r.value} for r in enum_map[resource_type]]
