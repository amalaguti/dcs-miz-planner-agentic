"""Build known catalog snapshots from packaged YAML + Spec enums."""

from __future__ import annotations

import json
from datetime import UTC, datetime

from ..models import (
    Coalition,
    MissionType,
    ObjectiveType,
    StartType,
)
from ..registry import ChannelRegistry, get_channel_registry
from .models import (
    CatalogAircraft,
    CatalogAirfield,
    CatalogEnumRow,
    CatalogPayload,
    CatalogPlanningOption,
    CatalogSnapshot,
    CatalogStrikeUnit,
    CatalogTheatre,
    CatalogWeatherPreset,
)

# Curated Spec/PyDCS country ids used by checked-in examples (not a full DCS dump).
_KNOWN_COUNTRIES = ("UK", "ThirdReich")

SOURCE_LABEL = "channel_yaml+spec_enums"


def _class_ids_by_unit(planning_options: tuple[CatalogPlanningOption, ...]) -> dict[str, list[str]]:
    """Invert strike_target_class meta unit_ids/ship_ids → class id list per unit."""
    by_unit: dict[str, list[str]] = {}
    for opt in planning_options:
        if opt.family != "strike_target_class":
            continue
        try:
            meta = json.loads(opt.meta_json) if opt.meta_json else {}
        except json.JSONDecodeError:
            continue
        if not isinstance(meta, dict):
            continue
        ids: list[str] = []
        for key in ("unit_ids", "ship_ids"):
            raw = meta.get(key) or []
            if isinstance(raw, list):
                ids.extend(str(x) for x in raw)
        for unit_id in ids:
            bucket = by_unit.setdefault(unit_id, [])
            if opt.id not in bucket:
                bucket.append(opt.id)
    return by_unit


def build_snapshot_from_registry(
    registry: ChannelRegistry | None = None,
    *,
    synced_at: datetime | None = None,
) -> CatalogSnapshot:
    registry = registry if registry is not None else get_channel_registry()
    synced_at = synced_at if synced_at is not None else datetime.now(UTC)

    theatres = tuple(CatalogTheatre(t) for t in registry.list_theatres())

    airfields = tuple(
        CatalogAirfield(
            name=name,
            airdrome_id=registry.airdrome_id(name, theatre=theatre_id),
            theatre_id=theatre_id,
        )
        for theatre_id in registry.list_theatres()
        for name in registry.list_airfields(theatre=theatre_id)
    )
    aircraft = tuple(
        CatalogAircraft(aid, registry.get_aircraft(aid).radio_mhz)
        for aid in registry.list_aircraft()
    )
    weather = tuple(
        CatalogWeatherPreset(p.name, p.description)
        for p in (registry.weather_preset(n) for n in registry.list_weather_presets())
    )
    payloads = tuple(
        CatalogPayload(
            name=name,
            meta_json=json.dumps(registry.payload_meta(name), sort_keys=True),
        )
        for name in registry.list_payloads()
    )
    planning_options = tuple(
        CatalogPlanningOption(
            family=opt.family,
            id=opt.id,
            label=opt.label,
            description=opt.description,
            support=opt.support,
            meta_json=json.dumps(opt.meta, sort_keys=True),
        )
        for opt in registry.list_planning_options()
    )
    class_map = _class_ids_by_unit(planning_options)
    # Strike shelves remain Channel-curated until a Normandy target batch ships.
    strike_theatre = (
        "TheChannel"
        if "TheChannel" in registry.list_theatres()
        else (theatres[0].theatre_id if theatres else "TheChannel")
    )
    strike_units = tuple(
        CatalogStrikeUnit(
            unit_id=uid,
            label=ref.label or uid,
            domain=ref.domain,
            theatre_id=strike_theatre,
            class_ids_json=json.dumps(class_map.get(uid, []), sort_keys=True),
        )
        for uid in registry.list_strike_units()
        for ref in (registry.get_strike_unit(uid),)
    )

    return CatalogSnapshot(
        synced_at=synced_at,
        source=SOURCE_LABEL,
        theatres=theatres,
        airfields=airfields,
        aircraft=aircraft,
        weather_presets=weather,
        payloads=payloads,
        planning_options=planning_options,
        strike_units=strike_units,
        mission_types=tuple(CatalogEnumRow(m.value) for m in MissionType),
        start_types=tuple(CatalogEnumRow(s.value) for s in StartType),
        coalitions=tuple(CatalogEnumRow(c.value) for c in Coalition),
        objective_types=tuple(CatalogEnumRow(o.value) for o in ObjectiveType),
        countries=tuple(CatalogEnumRow(c) for c in _KNOWN_COUNTRIES),
    )
