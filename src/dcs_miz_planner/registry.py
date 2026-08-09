"""Channel reference registry — queryable source of truth for DCS ids.

YAML under ``data/channel/`` is the committed artifact; this module loads it and
exposes lookups for the compiler (and later validator / agent tools).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any

import yaml


class RegistryError(KeyError):
    """Raised when a registry lookup fails with a clear, actionable message."""


@dataclass(frozen=True)
class AircraftRef:
    """Known Channel aircraft entry."""

    id: str
    radio_mhz: float


@dataclass(frozen=True)
class AircraftFailureRef:
    """Curated ME Set Failure id for a known aircraft."""

    id: str
    label: str
    family: str = ""


@dataclass(frozen=True)
class WeatherPresetRef:
    """Named weather preset known to the Mission Spec (optional compile recipe)."""

    name: str
    description: str = ""
    cloud_preset: str | None = None
    clouds_base_m: float | None = None
    clouds_thickness_m: float | None = None
    clouds_density: int | None = None
    enable_fog: bool | None = None
    fog_thickness: float | None = None
    fog_visibility: float | None = None
    visibility_distance: float | None = None
    temperature_c: float | None = None
    qnh_mmhg: float | None = None
    turbulence: float | None = None
    wind_ground_speed_ms: float | None = None
    wind_ground_dir_deg: float | None = None
    gallery_family: tuple[str, ...] = ()


@dataclass(frozen=True)
class PlanningOptionRef:
    """Curated planning knob for agent/CLI discovery (not a DCS type id)."""

    family: str
    id: str
    label: str
    description: str
    support: str  # supported | advisory | future
    meta: dict[str, Any]


@dataclass(frozen=True)
class GroundUnitRef:
    """Known Channel land strike target (exact DCS / PyDCS vehicle type id)."""

    id: str
    label: str = ""
    domain: str = "land"


@dataclass(frozen=True)
class ShipRef:
    """Known Channel sea strike target (exact DCS / PyDCS ship type id)."""

    id: str
    label: str = ""
    domain: str = "sea"


@dataclass(frozen=True)
class StrikeUnitRef:
    """Land or sea strike target resolved from the Channel registry."""

    id: str
    domain: str  # land | sea
    label: str = ""


@dataclass(frozen=True)
class PayloadPylon:
    """One pylon/CLSID pair in a named payload preset."""

    pylon: int
    clsid: str


@dataclass(frozen=True)
class PayloadRef:
    """Named payload preset with verified CLSIDs for one aircraft."""

    name: str
    aircraft: str
    label: str
    pylons: tuple[PayloadPylon, ...]


_VALID_SUPPORT = frozenset({"supported", "advisory", "future"})


def _load_yaml(name: str) -> dict[str, Any]:
    root = resources.files("dcs_miz_planner.data.channel")
    text = (root / name).read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise RegistryError(f"Channel registry file {name!r} must be a mapping")
    return data


class ChannelRegistry:
    """In-memory Channel Map reference data."""

    def __init__(
        self,
        *,
        airfields: dict[str, int],
        aircraft: dict[str, AircraftRef],
        theatres: frozenset[str],
        weather_presets: dict[str, WeatherPresetRef],
        payloads: dict[str, PayloadRef] | None = None,
        ground_units: dict[str, GroundUnitRef] | None = None,
        ships: dict[str, ShipRef] | None = None,
        planning_options: tuple[PlanningOptionRef, ...] | None = None,
        aircraft_failures: dict[str, tuple[AircraftFailureRef, ...]] | None = None,
        airfield_theatres: dict[str, str] | None = None,
    ) -> None:
        self._airfields = dict(airfields)
        self._aircraft = dict(aircraft)
        self._theatres = frozenset(theatres)
        self._weather_presets = dict(weather_presets)
        self._payloads = dict(payloads or {})
        self._ground_units = dict(ground_units or {})
        self._ships = dict(ships or {})
        self._planning_options = tuple(planning_options or ())
        self._aircraft_failures = {str(k): tuple(v) for k, v in (aircraft_failures or {}).items()}
        self._airfield_theatres = dict(airfield_theatres or {})

    @classmethod
    def from_packaged_yaml(cls) -> ChannelRegistry:
        airfields_doc = _load_yaml("airfields.yaml")
        airfields_raw = airfields_doc.get("airfields") or {}
        if not isinstance(airfields_raw, dict):
            raise RegistryError("airfields.yaml: 'airfields' must be a mapping")
        airfields = {str(k): int(v) for k, v in airfields_raw.items()}

        theatres_map_raw = airfields_doc.get("airfield_theatres") or {}
        if theatres_map_raw and not isinstance(theatres_map_raw, dict):
            raise RegistryError("airfields.yaml: 'airfield_theatres' must be a mapping")
        airfield_theatres = {str(k): str(v) for k, v in dict(theatres_map_raw).items()}
        unknown_af = sorted(set(airfield_theatres) - set(airfields))
        if unknown_af:
            raise RegistryError(
                f"airfields.yaml: airfield_theatres keys not in airfields: {unknown_af}"
            )

        aircraft_raw = _load_yaml("aircraft.yaml").get("aircraft") or {}
        if not isinstance(aircraft_raw, dict):
            raise RegistryError("aircraft.yaml: 'aircraft' must be a mapping")
        aircraft: dict[str, AircraftRef] = {}
        for aircraft_id, meta in aircraft_raw.items():
            if not isinstance(meta, dict) or "radio_mhz" not in meta:
                raise RegistryError(
                    f"aircraft.yaml: {aircraft_id!r} must map to {{radio_mhz: ...}}"
                )
            aircraft[str(aircraft_id)] = AircraftRef(
                id=str(aircraft_id),
                radio_mhz=float(meta["radio_mhz"]),
            )

        theatres_raw = _load_yaml("theatres.yaml").get("theatres") or []
        if not isinstance(theatres_raw, list):
            raise RegistryError("theatres.yaml: 'theatres' must be a list")
        theatres = frozenset(str(t) for t in theatres_raw)
        unknown_theatre = sorted(set(airfield_theatres.values()) - set(theatres))
        if unknown_theatre:
            raise RegistryError(
                f"airfields.yaml: airfield_theatres values not in theatres.yaml: {unknown_theatre}"
            )

        presets_raw = _load_yaml("weather_presets.yaml").get("presets") or {}
        if not isinstance(presets_raw, dict):
            raise RegistryError("weather_presets.yaml: 'presets' must be a mapping")
        weather_presets = {
            str(name): _parse_weather_preset(str(name), meta) for name, meta in presets_raw.items()
        }

        payloads_raw = _load_yaml("payloads.yaml").get("payloads") or {}
        if not isinstance(payloads_raw, dict):
            raise RegistryError("payloads.yaml: 'payloads' must be a mapping")
        payloads = {
            str(name): _parse_payload(str(name), meta) for name, meta in payloads_raw.items()
        }

        ground_raw = _load_yaml("ground_units.yaml").get("ground_units") or {}
        if not isinstance(ground_raw, dict):
            raise RegistryError("ground_units.yaml: 'ground_units' must be a mapping")
        ground_units: dict[str, GroundUnitRef] = {}
        for unit_id, meta in ground_raw.items():
            ground_units[str(unit_id)] = _parse_ground_unit(str(unit_id), meta)

        ships_raw = _load_yaml("ships.yaml").get("ships") or {}
        if not isinstance(ships_raw, dict):
            raise RegistryError("ships.yaml: 'ships' must be a mapping")
        ships: dict[str, ShipRef] = {}
        for ship_id, meta in ships_raw.items():
            ships[str(ship_id)] = _parse_ship(str(ship_id), meta)

        options_raw = _load_yaml("planning_options.yaml").get("options") or []
        if not isinstance(options_raw, list):
            raise RegistryError("planning_options.yaml: 'options' must be a list")
        planning_options = tuple(_parse_planning_option(row) for row in options_raw)

        failures_raw = _load_yaml("aircraft_failures.yaml").get("aircraft") or {}
        if not isinstance(failures_raw, dict):
            raise RegistryError("aircraft_failures.yaml: 'aircraft' must be a mapping")
        aircraft_failures: dict[str, tuple[AircraftFailureRef, ...]] = {}
        for aircraft_id, rows in failures_raw.items():
            if not isinstance(rows, list):
                raise RegistryError(f"aircraft_failures.yaml: {aircraft_id!r} must map to a list")
            aircraft_failures[str(aircraft_id)] = tuple(
                _parse_aircraft_failure(row) for row in rows
            )

        return cls(
            airfields=airfields,
            airfield_theatres=airfield_theatres,
            aircraft=aircraft,
            theatres=theatres,
            weather_presets=weather_presets,
            payloads=payloads,
            ground_units=ground_units,
            ships=ships,
            planning_options=planning_options,
            aircraft_failures=aircraft_failures,
        )

    def airdrome_id(self, name: str) -> int:
        try:
            return self._airfields[name]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown Channel airfield '{name}'. Known: {sorted(self._airfields)}"
            ) from exc

    def list_airfields(self) -> list[str]:
        return sorted(self._airfields)

    def airfield_theatre(self, name: str) -> str:
        """Theatre id for catalog tagging; default ``TheChannel`` when unset."""
        if name not in self._airfields:
            raise RegistryError(
                f"Unknown Channel airfield '{name}'. Known: {sorted(self._airfields)}"
            )
        mapped = self._airfield_theatres.get(name)
        if mapped is not None:
            return mapped
        if "TheChannel" in self._theatres:
            return "TheChannel"
        # Single-theatre test registries without TheChannel.
        return min(self._theatres) if self._theatres else "TheChannel"

    def get_aircraft(self, aircraft_id: str) -> AircraftRef:
        try:
            return self._aircraft[aircraft_id]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown aircraft '{aircraft_id}'. Known: {sorted(self._aircraft)}"
            ) from exc

    def radio_mhz(self, aircraft_id: str) -> float:
        return self.get_aircraft(aircraft_id).radio_mhz

    def list_aircraft(self) -> list[str]:
        return sorted(self._aircraft)

    def known_aircraft(self) -> frozenset[str]:
        return frozenset(self._aircraft)

    def list_failures(self, aircraft_id: str) -> tuple[AircraftFailureRef, ...]:
        return self._aircraft_failures.get(aircraft_id, ())

    def is_known_failure(self, aircraft_id: str, failure_id: str) -> bool:
        return any(f.id == failure_id for f in self.list_failures(aircraft_id))

    def get_failure(self, aircraft_id: str, failure_id: str) -> AircraftFailureRef:
        for ref in self.list_failures(aircraft_id):
            if ref.id == failure_id:
                return ref
        known = [f.id for f in self.list_failures(aircraft_id)]
        raise RegistryError(
            f"Unknown failure {failure_id!r} for aircraft {aircraft_id!r}. Known: {known}"
        )

    def has_theatre(self, theatre_id: str) -> bool:
        return theatre_id in self._theatres

    def list_theatres(self) -> list[str]:
        return sorted(self._theatres)

    def weather_preset(self, name: str) -> WeatherPresetRef:
        try:
            return self._weather_presets[name]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown weather preset '{name}'. Known: {sorted(self._weather_presets)}"
            ) from exc

    def list_weather_presets(self) -> list[str]:
        return sorted(self._weather_presets)

    def list_payloads(self) -> list[str]:
        return sorted(self._payloads)

    def get_payload(self, name: str) -> PayloadRef:
        try:
            return self._payloads[name]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown payload '{name}'. Known: {sorted(self._payloads)}"
            ) from exc

    def payload_meta(self, name: str) -> dict[str, Any]:
        """JSON-serialisable preset meta (catalog sync / tooling)."""
        ref = self.get_payload(name)
        return {
            "aircraft": ref.aircraft,
            "label": ref.label,
            "pylons": [{"pylon": p.pylon, "clsid": p.clsid} for p in ref.pylons],
        }

    def list_ground_units(self) -> list[str]:
        return sorted(self._ground_units)

    def get_ground_unit(self, unit_id: str) -> GroundUnitRef:
        try:
            return self._ground_units[unit_id]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown ground unit '{unit_id}'. Known: {sorted(self._ground_units)}"
            ) from exc

    def known_ground_units(self) -> frozenset[str]:
        return frozenset(self._ground_units)

    def list_ships(self) -> list[str]:
        return sorted(self._ships)

    def get_ship(self, ship_id: str) -> ShipRef:
        try:
            return self._ships[ship_id]
        except KeyError as exc:
            raise RegistryError(f"Unknown ship '{ship_id}'. Known: {sorted(self._ships)}") from exc

    def get_strike_unit(self, unit_id: str) -> StrikeUnitRef:
        """Resolve a land or sea strike target id."""
        if unit_id in self._ground_units:
            g = self._ground_units[unit_id]
            return StrikeUnitRef(id=g.id, domain="land", label=g.label)
        if unit_id in self._ships:
            s = self._ships[unit_id]
            return StrikeUnitRef(id=s.id, domain="sea", label=s.label)
        known = sorted(set(self._ground_units) | set(self._ships))
        raise RegistryError(f"Unknown strike target '{unit_id}'. Known: {known}")

    def list_strike_units(self) -> list[str]:
        return sorted(set(self._ground_units) | set(self._ships))

    def list_planning_options(self) -> tuple[PlanningOptionRef, ...]:
        return self._planning_options


def _parse_weather_preset(name: str, meta: Any) -> WeatherPresetRef:
    if meta is None:
        return WeatherPresetRef(name=name)
    if not isinstance(meta, dict):
        raise RegistryError(f"weather_presets.yaml: {name!r} must map to a mapping")

    def _opt_float(key: str) -> float | None:
        if key not in meta or meta[key] is None:
            return None
        return float(meta[key])

    def _opt_int(key: str) -> int | None:
        if key not in meta or meta[key] is None:
            return None
        return int(meta[key])

    def _opt_bool(key: str) -> bool | None:
        if key not in meta or meta[key] is None:
            return None
        return bool(meta[key])

    cloud = meta.get("cloud_preset")
    family_raw = meta.get("gallery_family")
    family: tuple[str, ...] = ()
    if family_raw is not None:
        if not isinstance(family_raw, list) or not all(isinstance(x, str) for x in family_raw):
            raise RegistryError(
                f"weather_presets.yaml: {name!r} gallery_family must be a string list"
            )
        family = tuple(str(x) for x in family_raw)
    return WeatherPresetRef(
        name=name,
        description=str(meta.get("description") or ""),
        cloud_preset=str(cloud) if cloud else None,
        clouds_base_m=_opt_float("clouds_base_m"),
        clouds_thickness_m=_opt_float("clouds_thickness_m"),
        clouds_density=_opt_int("clouds_density"),
        enable_fog=_opt_bool("enable_fog"),
        fog_thickness=_opt_float("fog_thickness"),
        fog_visibility=_opt_float("fog_visibility"),
        visibility_distance=_opt_float("visibility_distance"),
        temperature_c=_opt_float("temperature_c"),
        qnh_mmhg=_opt_float("qnh_mmhg"),
        turbulence=_opt_float("turbulence"),
        wind_ground_speed_ms=_opt_float("wind_ground_speed_ms"),
        wind_ground_dir_deg=_opt_float("wind_ground_dir_deg"),
        gallery_family=family,
    )


def _parse_ground_unit(unit_id: str, meta: Any) -> GroundUnitRef:
    if meta is None:
        return GroundUnitRef(id=unit_id, domain="land")
    if not isinstance(meta, dict):
        raise RegistryError(f"ground_units.yaml: {unit_id!r} must map to a mapping")
    domain = str(meta.get("domain") or "land").strip()
    if domain != "land":
        raise RegistryError(f"ground_units.yaml: {unit_id!r} domain must be 'land'")
    return GroundUnitRef(id=unit_id, label=str(meta.get("label") or ""), domain="land")


def _parse_ship(ship_id: str, meta: Any) -> ShipRef:
    if meta is None:
        return ShipRef(id=ship_id, domain="sea")
    if not isinstance(meta, dict):
        raise RegistryError(f"ships.yaml: {ship_id!r} must map to a mapping")
    domain = str(meta.get("domain") or "sea").strip()
    if domain != "sea":
        raise RegistryError(f"ships.yaml: {ship_id!r} domain must be 'sea'")
    return ShipRef(id=ship_id, label=str(meta.get("label") or ""), domain="sea")


def _parse_aircraft_failure(meta: Any) -> AircraftFailureRef:
    if not isinstance(meta, dict):
        raise RegistryError("aircraft_failures.yaml: each entry must be a mapping")
    failure_id = str(meta.get("id") or "").strip()
    if not failure_id:
        raise RegistryError("aircraft_failures.yaml: entry requires id")
    return AircraftFailureRef(
        id=failure_id,
        label=str(meta.get("label") or failure_id),
        family=str(meta.get("family") or ""),
    )


def _parse_payload(name: str, meta: Any) -> PayloadRef:
    if not isinstance(meta, dict):
        raise RegistryError(f"payloads.yaml: {name!r} must map to a mapping")
    aircraft = str(meta.get("aircraft") or "").strip()
    if not aircraft:
        raise RegistryError(f"payloads.yaml: {name!r} requires aircraft")
    label = str(meta.get("label") or name)
    pylons_raw = meta.get("pylons") or []
    if not isinstance(pylons_raw, list) or not pylons_raw:
        raise RegistryError(f"payloads.yaml: {name!r} requires a non-empty pylons list")
    pylons: list[PayloadPylon] = []
    for i, row in enumerate(pylons_raw):
        if not isinstance(row, dict):
            raise RegistryError(f"payloads.yaml: {name!r} pylons[{i}] must be a mapping")
        try:
            pylon = int(row["pylon"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RegistryError(f"payloads.yaml: {name!r} pylons[{i}] needs integer pylon") from exc
        clsid = str(row.get("clsid") or "").strip()
        if not clsid:
            raise RegistryError(f"payloads.yaml: {name!r} pylons[{i}] needs clsid")
        pylons.append(PayloadPylon(pylon=pylon, clsid=clsid))
    return PayloadRef(name=name, aircraft=aircraft, label=label, pylons=tuple(pylons))


def _parse_planning_option(row: Any) -> PlanningOptionRef:
    if not isinstance(row, dict):
        raise RegistryError("planning_options.yaml: each option must be a mapping")
    family = str(row.get("family") or "").strip()
    option_id = str(row.get("id") or "").strip()
    label = str(row.get("label") or "").strip()
    description = str(row.get("description") or "").strip()
    support = str(row.get("support") or "").strip()
    if not family or not option_id or not label:
        raise RegistryError("planning_options.yaml: each option needs family, id, and label")
    if support not in _VALID_SUPPORT:
        raise RegistryError(
            f"planning_options.yaml: {family}/{option_id} support must be one of "
            f"{sorted(_VALID_SUPPORT)}, got {support!r}"
        )
    meta_raw = row.get("meta") or {}
    if not isinstance(meta_raw, dict):
        raise RegistryError(f"planning_options.yaml: {family}/{option_id} meta must be a mapping")
    return PlanningOptionRef(
        family=family,
        id=option_id,
        label=label,
        description=description,
        support=support,
        meta=dict(meta_raw),
    )


@lru_cache(maxsize=1)
def get_channel_registry() -> ChannelRegistry:
    """Return the packaged Channel registry (loaded once)."""
    return ChannelRegistry.from_packaged_yaml()
