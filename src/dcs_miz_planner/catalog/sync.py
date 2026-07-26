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
    CatalogSnapshot,
    CatalogTheatre,
    CatalogWeatherPreset,
)

# Curated Spec/PyDCS country ids used by checked-in examples (not a full DCS dump).
_KNOWN_COUNTRIES = ("UK", "ThirdReich")

SOURCE_LABEL = "channel_yaml+spec_enums"


def build_snapshot_from_registry(
    registry: ChannelRegistry | None = None,
    *,
    synced_at: datetime | None = None,
) -> CatalogSnapshot:
    registry = registry if registry is not None else get_channel_registry()
    synced_at = synced_at if synced_at is not None else datetime.now(UTC)

    theatres = tuple(CatalogTheatre(t) for t in registry.list_theatres())
    theatre_id = theatres[0].theatre_id if theatres else "TheChannel"

    airfields = tuple(
        CatalogAirfield(name=name, airdrome_id=registry.airdrome_id(name), theatre_id=theatre_id)
        for name in registry.list_airfields()
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

    return CatalogSnapshot(
        synced_at=synced_at,
        source=SOURCE_LABEL,
        theatres=theatres,
        airfields=airfields,
        aircraft=aircraft,
        weather_presets=weather,
        payloads=payloads,
        mission_types=tuple(CatalogEnumRow(m.value) for m in MissionType),
        start_types=tuple(CatalogEnumRow(s.value) for s in StartType),
        coalitions=tuple(CatalogEnumRow(c.value) for c in Coalition),
        objective_types=tuple(CatalogEnumRow(o.value) for o in ObjectiveType),
        countries=tuple(CatalogEnumRow(c) for c in _KNOWN_COUNTRIES),
    )
