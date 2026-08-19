"""Packaged reference registry — queryable source of truth for DCS ids.

YAML under ``data/era/``, ``data/shared/``, and ``data/theatres/<SpecId>/`` is the
committed artifact; this module loads it and exposes lookups for the compiler
(and later validator / agent tools).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from typing import Any

import yaml

_DATA_PACKAGE = "dcs_miz_planner.data"
_KNOWN_ERAS = frozenset({"wwii", "modern"})


class RegistryError(KeyError):
    """Raised when a registry lookup fails with a clear, actionable message."""


@dataclass(frozen=True)
class AircraftRef:
    """Known Channel aircraft entry."""

    id: str
    radio_mhz: float
    radio_channels_mhz: tuple[float, ...] = ()


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
    """Known land strike target (exact DCS / PyDCS vehicle type id)."""

    id: str
    label: str = ""
    domain: str = "land"
    era: str = "wwii"


@dataclass(frozen=True)
class ShipRef:
    """Known Channel sea strike target (exact DCS / PyDCS ship type id)."""

    id: str
    label: str = ""
    domain: str = "sea"


@dataclass(frozen=True)
class StaticObjectRef:
    """Known ME static/fortification type (exact PyDCS fortification_map key)."""

    id: str
    label: str = ""


@dataclass(frozen=True)
class StrikeUnitRef:
    """Land or sea strike target resolved from the Channel registry."""

    id: str
    domain: str  # land | sea
    label: str = ""
    era: str = "wwii"


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


def _data_root():
    return resources.files(_DATA_PACKAGE)


def _load_yaml_file(path: Any, label: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise RegistryError(f"{label} must be a mapping")
    return data


def _partition_airfields(
    airfields: dict[str, int],
    airfield_theatres: dict[str, str],
    theatres: frozenset[str],
) -> dict[str, dict[str, int]]:
    """Split a flat test constructor map into per-theatre airfield tables."""
    unknown_af = sorted(set(airfield_theatres) - set(airfields))
    if unknown_af:
        raise RegistryError(f"airfield_theatres keys not in airfields: {unknown_af}")
    unknown_theatre = sorted(set(airfield_theatres.values()) - set(theatres))
    if unknown_theatre:
        raise RegistryError(f"airfield_theatres values not in theatres: {unknown_theatre}")
    by_theatre: dict[str, dict[str, int]] = {t: {} for t in theatres}
    for name, aid in airfields.items():
        mapped = airfield_theatres.get(name)
        if mapped is not None:
            theatre = mapped
        elif "TheChannel" in theatres:
            theatre = "TheChannel"
        else:
            theatre = min(theatres) if theatres else "TheChannel"
        by_theatre.setdefault(theatre, {})[str(name)] = int(aid)
    return by_theatre


def _load_theatre_packages(
    theatres_root: Any,
) -> tuple[dict[str, dict[str, int]], frozenset[str], dict[str, str]]:
    """Walk ``data/theatres/<SpecId>/`` and load per-theatre airfield maps + era."""
    if not theatres_root.is_dir():
        raise RegistryError("packaged data/theatres/ is missing")
    by_theatre: dict[str, dict[str, int]] = {}
    theatre_eras: dict[str, str] = {}
    for child in theatres_root.iterdir():
        name = child.name
        if not child.is_dir() or name.startswith((".", "__")):
            continue
        theatre_file = child / "theatre.yaml"
        if not theatre_file.is_file():
            raise RegistryError(f"theatres/{name}: missing theatre.yaml")
        doc = _load_yaml_file(theatre_file, f"theatres/{name}/theatre.yaml")
        theatre_id = str(doc.get("id") or "").strip()
        era_id = str(doc.get("era") or "").strip()
        if theatre_id != name:
            raise RegistryError(
                f"theatres/{name}: theatre.yaml id {theatre_id!r} must match folder name"
            )
        if era_id not in _KNOWN_ERAS:
            raise RegistryError(
                f"theatres/{name}: unknown era {era_id!r} (expected one of {sorted(_KNOWN_ERAS)})"
            )
        af_file = child / "airfields.yaml"
        if not af_file.is_file():
            raise RegistryError(f"theatres/{name}: missing airfields.yaml")
        af_doc = _load_yaml_file(af_file, f"theatres/{name}/airfields.yaml")
        airfields_raw = af_doc.get("airfields") or {}
        if not isinstance(airfields_raw, dict):
            raise RegistryError(f"theatres/{name}/airfields.yaml: 'airfields' must be a mapping")
        if not airfields_raw:
            raise RegistryError(f"theatres/{name}: airfields.yaml is empty")
        mapping: dict[str, int] = {}
        for key, value in airfields_raw.items():
            af_name = str(key)
            if af_name in mapping:
                raise RegistryError(f"theatres/{name}: duplicate airfield {af_name!r}")
            mapping[af_name] = int(value)
        by_theatre[theatre_id] = mapping
        theatre_eras[theatre_id] = era_id
    if not by_theatre:
        raise RegistryError("no theatre packages found under data/theatres/")
    return by_theatre, frozenset(by_theatre), theatre_eras


def _parse_countries_doc(doc: dict[str, Any], label: str) -> frozenset[str]:
    countries_raw = doc.get("countries") or {}
    if isinstance(countries_raw, dict):
        countries = frozenset(str(k) for k in countries_raw)
    elif isinstance(countries_raw, list):
        countries = frozenset(str(x) for x in countries_raw)
    else:
        raise RegistryError(f"{label}: 'countries' must be a mapping or list")
    if not countries:
        raise RegistryError(f"{label}: 'countries' is empty")
    if "Germany" in countries:
        raise RegistryError("Germany must not be a known country id (hint to ThirdReich)")
    return countries


def _parse_aircraft_doc(doc: dict[str, Any], label: str) -> dict[str, AircraftRef]:
    aircraft_raw = doc.get("aircraft") or {}
    if not isinstance(aircraft_raw, dict):
        raise RegistryError(f"{label}: 'aircraft' must be a mapping")
    aircraft: dict[str, AircraftRef] = {}
    for aircraft_id, meta in aircraft_raw.items():
        if not isinstance(meta, dict) or "radio_mhz" not in meta:
            raise RegistryError(f"{label}: {aircraft_id!r} must map to {{radio_mhz: ...}}")
        radio_mhz = float(meta["radio_mhz"])
        channels_raw = meta.get("radio_channels_mhz")
        channels: tuple[float, ...] = ()
        if channels_raw is not None:
            if not isinstance(channels_raw, list) or not channels_raw:
                raise RegistryError(
                    f"{label}: {aircraft_id!r} radio_channels_mhz must be a non-empty list"
                )
            channels = tuple(float(x) for x in channels_raw)
            if abs(channels[0] - radio_mhz) > 0.01:
                raise RegistryError(
                    f"{label}: {aircraft_id!r} radio_channels_mhz[0] must equal radio_mhz"
                )
        aircraft[str(aircraft_id)] = AircraftRef(
            id=str(aircraft_id),
            radio_mhz=radio_mhz,
            radio_channels_mhz=channels,
        )
    return aircraft


def _load_era_identity(
    era_root: Any,
) -> tuple[dict[str, frozenset[str]], dict[str, dict[str, AircraftRef]], dict[str, AircraftRef]]:
    """Walk ``data/era/<era>/`` for countries.yaml + aircraft.yaml (era-keyed)."""
    if not era_root.is_dir():
        raise RegistryError("packaged data/era/ is missing")
    countries_by_era: dict[str, frozenset[str]] = {}
    aircraft_by_era: dict[str, dict[str, AircraftRef]] = {}
    aircraft_merged: dict[str, AircraftRef] = {}
    for child in era_root.iterdir():
        era_id = child.name
        if not child.is_dir() or era_id.startswith((".", "__")):
            continue
        if era_id not in _KNOWN_ERAS:
            raise RegistryError(
                f"era/{era_id}: unknown era (expected one of {sorted(_KNOWN_ERAS)})"
            )
        countries_file = child / "countries.yaml"
        aircraft_file = child / "aircraft.yaml"
        if not countries_file.is_file():
            raise RegistryError(f"era/{era_id}: missing countries.yaml")
        if not aircraft_file.is_file():
            raise RegistryError(f"era/{era_id}: missing aircraft.yaml")
        countries = _parse_countries_doc(
            _load_yaml_file(countries_file, f"era/{era_id}/countries.yaml"),
            f"era/{era_id}/countries.yaml",
        )
        aircraft = _parse_aircraft_doc(
            _load_yaml_file(aircraft_file, f"era/{era_id}/aircraft.yaml"),
            f"era/{era_id}/aircraft.yaml",
        )
        countries_by_era[era_id] = countries
        aircraft_by_era[era_id] = aircraft
        for aid, ref in aircraft.items():
            existing = aircraft_merged.get(aid)
            if existing is not None and existing != ref:
                raise RegistryError(f"era/{era_id}: aircraft id {aid!r} collides with another era")
            aircraft_merged[aid] = ref
    if not countries_by_era:
        raise RegistryError("no era packages found under data/era/")
    return countries_by_era, aircraft_by_era, aircraft_merged


class ChannelRegistry:
    """In-memory packaged reference data (era + shared + per-theatre)."""

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
        static_objects: dict[str, StaticObjectRef] | None = None,
        airfield_theatres: dict[str, str] | None = None,
        airfields_by_theatre: dict[str, dict[str, int]] | None = None,
        theatre_eras: dict[str, str] | None = None,
        countries: frozenset[str] | None = None,
        countries_by_era: dict[str, frozenset[str]] | None = None,
        aircraft_by_era: dict[str, dict[str, AircraftRef]] | None = None,
    ) -> None:
        self._aircraft = dict(aircraft)
        self._theatres = frozenset(theatres)
        self._weather_presets = dict(weather_presets)
        self._payloads = dict(payloads or {})
        self._ground_units = dict(ground_units or {})
        self._ships = dict(ships or {})
        self._planning_options = tuple(planning_options or ())
        self._aircraft_failures = {str(k): tuple(v) for k, v in (aircraft_failures or {}).items()}
        self._static_objects = dict(static_objects or {})
        if theatre_eras is not None:
            self._theatre_eras = {str(k): str(v) for k, v in theatre_eras.items()}
        else:
            self._theatre_eras = {t: "wwii" for t in self._theatres}
        if countries_by_era is not None:
            self._countries_by_era = {str(k): frozenset(v) for k, v in countries_by_era.items()}
            union: set[str] = set()
            for names in self._countries_by_era.values():
                union.update(names)
            self._countries = frozenset(union)
        else:
            self._countries = (
                frozenset(countries) if countries is not None else frozenset({"UK", "ThirdReich"})
            )
            self._countries_by_era = {"wwii": self._countries}
        if aircraft_by_era is not None:
            self._aircraft_by_era = {
                str(k): {str(aid): ref for aid, ref in mapping.items()}
                for k, mapping in aircraft_by_era.items()
            }
            for mapping in self._aircraft_by_era.values():
                for aid, ref in mapping.items():
                    self._aircraft.setdefault(aid, ref)
        else:
            self._aircraft_by_era = {"wwii": dict(self._aircraft)}
        if airfields_by_theatre is not None:
            self._airfields_by_theatre = {
                str(tid): {str(n): int(aid) for n, aid in mapping.items()}
                for tid, mapping in airfields_by_theatre.items()
            }
        else:
            self._airfields_by_theatre = _partition_airfields(
                airfields, dict(airfield_theatres or {}), self._theatres
            )

    @classmethod
    def from_packaged_packages(cls) -> ChannelRegistry:
        root = _data_root()
        era_root = root / "era"
        wwii_root = era_root / "wwii"
        shared_root = root / "shared"

        countries_by_era, aircraft_by_era, aircraft = _load_era_identity(era_root)

        presets_raw = (
            _load_yaml_file(
                shared_root / "weather_presets.yaml", "shared/weather_presets.yaml"
            ).get("presets")
            or {}
        )
        if not isinstance(presets_raw, dict):
            raise RegistryError("weather_presets.yaml: 'presets' must be a mapping")
        weather_presets = {
            str(name): _parse_weather_preset(str(name), meta) for name, meta in presets_raw.items()
        }

        payloads_raw = (
            _load_yaml_file(wwii_root / "payloads.yaml", "era/wwii/payloads.yaml").get("payloads")
            or {}
        )
        if not isinstance(payloads_raw, dict):
            raise RegistryError("payloads.yaml: 'payloads' must be a mapping")
        payloads = {
            str(name): _parse_payload(str(name), meta) for name, meta in payloads_raw.items()
        }
        modern_payloads_path = era_root / "modern" / "payloads.yaml"
        if modern_payloads_path.is_file():
            modern_payloads_raw = (
                _load_yaml_file(modern_payloads_path, "era/modern/payloads.yaml").get("payloads")
                or {}
            )
            if not isinstance(modern_payloads_raw, dict):
                raise RegistryError("era/modern/payloads.yaml: 'payloads' must be a mapping")
            for name, meta in modern_payloads_raw.items():
                parsed = _parse_payload(str(name), meta)
                existing = payloads.get(str(name))
                if existing is not None and existing != parsed:
                    raise RegistryError(f"era/modern: payload {name!r} collides with another era")
                payloads[str(name)] = parsed

        ground_raw = (
            _load_yaml_file(wwii_root / "ground_units.yaml", "era/wwii/ground_units.yaml").get(
                "ground_units"
            )
            or {}
        )
        if not isinstance(ground_raw, dict):
            raise RegistryError("ground_units.yaml: 'ground_units' must be a mapping")
        ground_units: dict[str, GroundUnitRef] = {}
        for unit_id, meta in ground_raw.items():
            ground_units[str(unit_id)] = _parse_ground_unit(str(unit_id), meta, era="wwii")
        modern_ground_path = era_root / "modern" / "ground_units.yaml"
        if modern_ground_path.is_file():
            modern_ground_raw = (
                _load_yaml_file(modern_ground_path, "era/modern/ground_units.yaml").get(
                    "ground_units"
                )
                or {}
            )
            if not isinstance(modern_ground_raw, dict):
                raise RegistryError(
                    "era/modern/ground_units.yaml: 'ground_units' must be a mapping"
                )
            for unit_id, meta in modern_ground_raw.items():
                parsed = _parse_ground_unit(str(unit_id), meta, era="modern")
                existing = ground_units.get(str(unit_id))
                if existing is not None and existing != parsed:
                    raise RegistryError(
                        f"era/modern: ground unit {unit_id!r} collides with another era"
                    )
                ground_units[str(unit_id)] = parsed

        ships_raw = (
            _load_yaml_file(wwii_root / "ships.yaml", "era/wwii/ships.yaml").get("ships") or {}
        )
        if not isinstance(ships_raw, dict):
            raise RegistryError("ships.yaml: 'ships' must be a mapping")
        ships: dict[str, ShipRef] = {}
        for ship_id, meta in ships_raw.items():
            ships[str(ship_id)] = _parse_ship(str(ship_id), meta)

        options_raw = (
            _load_yaml_file(
                shared_root / "planning_options.yaml", "shared/planning_options.yaml"
            ).get("options")
            or []
        )
        if not isinstance(options_raw, list):
            raise RegistryError("planning_options.yaml: 'options' must be a list")
        planning_options = tuple(_parse_planning_option(row) for row in options_raw)

        failures_raw = (
            _load_yaml_file(
                wwii_root / "aircraft_failures.yaml", "era/wwii/aircraft_failures.yaml"
            ).get("aircraft")
            or {}
        )
        if not isinstance(failures_raw, dict):
            raise RegistryError("aircraft_failures.yaml: 'aircraft' must be a mapping")
        aircraft_failures: dict[str, tuple[AircraftFailureRef, ...]] = {}
        for aircraft_id, rows in failures_raw.items():
            if not isinstance(rows, list):
                raise RegistryError(f"aircraft_failures.yaml: {aircraft_id!r} must map to a list")
            aircraft_failures[str(aircraft_id)] = tuple(
                _parse_aircraft_failure(row) for row in rows
            )

        statics_raw = (
            _load_yaml_file(wwii_root / "statics.yaml", "era/wwii/statics.yaml").get("statics")
            or {}
        )
        if not isinstance(statics_raw, dict):
            raise RegistryError("statics.yaml: 'statics' must be a mapping")
        static_objects = {
            str(sid): _parse_static_object(str(sid), meta) for sid, meta in statics_raw.items()
        }

        airfields_by_theatre, theatres, theatre_eras = _load_theatre_packages(root / "theatres")
        airfields: dict[str, int] = {}
        airfield_theatres: dict[str, str] = {}
        for tid, mapping in airfields_by_theatre.items():
            for af_name, aid in mapping.items():
                if af_name not in airfields:
                    airfields[af_name] = aid
                if tid != "TheChannel":
                    airfield_theatres[af_name] = tid

        return cls(
            airfields=airfields,
            airfield_theatres=airfield_theatres,
            airfields_by_theatre=airfields_by_theatre,
            aircraft=aircraft,
            theatres=theatres,
            theatre_eras=theatre_eras,
            countries_by_era=countries_by_era,
            aircraft_by_era=aircraft_by_era,
            weather_presets=weather_presets,
            payloads=payloads,
            ground_units=ground_units,
            ships=ships,
            planning_options=planning_options,
            aircraft_failures=aircraft_failures,
            static_objects=static_objects,
        )

    @classmethod
    def from_packaged_yaml(cls) -> ChannelRegistry:
        """Alias for :meth:`from_packaged_packages` (legacy name)."""
        return cls.from_packaged_packages()

    def airdrome_id(self, name: str, theatre: str | None = None) -> int:
        if theatre is not None:
            if theatre not in self._theatres:
                raise RegistryError(f"Unknown theatre '{theatre}'. Known: {sorted(self._theatres)}")
            mapping = self._airfields_by_theatre.get(theatre, {})
            try:
                return mapping[name]
            except KeyError as exc:
                raise RegistryError(f"Unknown airfield '{name}'. Known: {sorted(mapping)}") from exc
        owners = [
            (tid, mapping[name])
            for tid, mapping in self._airfields_by_theatre.items()
            if name in mapping
        ]
        if len(owners) == 1:
            return owners[0][1]
        if len(owners) > 1:
            theatres = sorted(tid for tid, _ in owners)
            raise RegistryError(
                f"Ambiguous airfield '{name}' (present in {theatres}). Pass theatre=."
            )
        known = sorted({n for mapping in self._airfields_by_theatre.values() for n in mapping})
        raise RegistryError(f"Unknown airfield '{name}'. Known: {known}")

    def list_airfields(self, theatre: str | None = None) -> list[str]:
        if theatre is not None:
            if theatre not in self._theatres:
                raise RegistryError(f"Unknown theatre '{theatre}'. Known: {sorted(self._theatres)}")
            return sorted(self._airfields_by_theatre.get(theatre, {}))
        names = {n for mapping in self._airfields_by_theatre.values() for n in mapping}
        return sorted(names)

    def airfield_theatre(self, name: str) -> str:
        """Theatre id for catalog tagging; unique-name lookup."""
        owners = [tid for tid, mapping in self._airfields_by_theatre.items() if name in mapping]
        if len(owners) == 1:
            return owners[0]
        if len(owners) > 1:
            raise RegistryError(
                f"Ambiguous airfield '{name}' (present in {sorted(owners)}). Pass theatre=."
            )
        known = sorted({n for mapping in self._airfields_by_theatre.values() for n in mapping})
        raise RegistryError(f"Unknown airfield '{name}'. Known: {known}")

    def get_aircraft(self, aircraft_id: str) -> AircraftRef:
        try:
            return self._aircraft[aircraft_id]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown aircraft '{aircraft_id}'. Known: {sorted(self._aircraft)}"
            ) from exc

    def radio_mhz(self, aircraft_id: str) -> float:
        return self.get_aircraft(aircraft_id).radio_mhz

    def radio_channels_mhz(self, aircraft_id: str) -> tuple[float, ...]:
        return self.get_aircraft(aircraft_id).radio_channels_mhz

    def list_aircraft(self, era: str | None = None) -> list[str]:
        return sorted(self.known_aircraft(era=era))

    def known_aircraft(self, era: str | None = None) -> frozenset[str]:
        if era is None:
            return frozenset(self._aircraft)
        if era not in self._aircraft_by_era:
            raise RegistryError(f"Unknown era '{era}'. Known: {sorted(self._aircraft_by_era)}")
        return frozenset(self._aircraft_by_era[era])

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

    def era_for_theatre(self, theatre_id: str) -> str:
        if theatre_id not in self._theatres:
            raise RegistryError(f"Unknown theatre '{theatre_id}'. Known: {sorted(self._theatres)}")
        era = self._theatre_eras.get(theatre_id)
        if not era:
            raise RegistryError(f"No era recorded for theatre '{theatre_id}'")
        return era

    def list_countries(self, era: str | None = None) -> list[str]:
        if era is None:
            return sorted(self._countries)
        if era not in self._countries_by_era:
            raise RegistryError(f"Unknown era '{era}'. Known: {sorted(self._countries_by_era)}")
        return sorted(self._countries_by_era[era])

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

    def list_statics(self) -> list[str]:
        return sorted(self._static_objects)

    def get_static(self, static_id: str) -> StaticObjectRef:
        try:
            return self._static_objects[static_id]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown static '{static_id}'. Known: {sorted(self._static_objects)}"
            ) from exc

    def known_statics(self) -> frozenset[str]:
        return frozenset(self._static_objects)

    def get_strike_unit(self, unit_id: str) -> StrikeUnitRef:
        """Resolve a land or sea strike target id."""
        if unit_id in self._ground_units:
            g = self._ground_units[unit_id]
            return StrikeUnitRef(id=g.id, domain="land", label=g.label, era=g.era)
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


def _parse_ground_unit(unit_id: str, meta: Any, *, era: str = "wwii") -> GroundUnitRef:
    if meta is None:
        return GroundUnitRef(id=unit_id, domain="land", era=era)
    if not isinstance(meta, dict):
        raise RegistryError(f"ground_units.yaml: {unit_id!r} must map to a mapping")
    domain = str(meta.get("domain") or "land").strip()
    if domain != "land":
        raise RegistryError(f"ground_units.yaml: {unit_id!r} domain must be 'land'")
    return GroundUnitRef(id=unit_id, label=str(meta.get("label") or ""), domain="land", era=era)


def _parse_ship(ship_id: str, meta: Any) -> ShipRef:
    if meta is None:
        return ShipRef(id=ship_id, domain="sea")
    if not isinstance(meta, dict):
        raise RegistryError(f"ships.yaml: {ship_id!r} must map to a mapping")
    domain = str(meta.get("domain") or "sea").strip()
    if domain != "sea":
        raise RegistryError(f"ships.yaml: {ship_id!r} domain must be 'sea'")
    return ShipRef(id=ship_id, label=str(meta.get("label") or ""), domain="sea")


def _parse_static_object(static_id: str, meta: Any) -> StaticObjectRef:
    if meta is None:
        return StaticObjectRef(id=static_id)
    if not isinstance(meta, dict):
        raise RegistryError(f"statics.yaml: {static_id!r} must map to a mapping")
    return StaticObjectRef(id=static_id, label=str(meta.get("label") or ""))


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
    return ChannelRegistry.from_packaged_packages()
