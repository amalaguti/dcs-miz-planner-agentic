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
class WeatherPresetRef:
    """Named weather preset known to the Mission Spec."""

    name: str
    description: str = ""


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
        payloads: dict[str, Any] | None = None,
    ) -> None:
        self._airfields = dict(airfields)
        self._aircraft = dict(aircraft)
        self._theatres = frozenset(theatres)
        self._weather_presets = dict(weather_presets)
        self._payloads = dict(payloads or {})

    @classmethod
    def from_packaged_yaml(cls) -> ChannelRegistry:
        airfields_raw = _load_yaml("airfields.yaml").get("airfields") or {}
        if not isinstance(airfields_raw, dict):
            raise RegistryError("airfields.yaml: 'airfields' must be a mapping")
        airfields = {str(k): int(v) for k, v in airfields_raw.items()}

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

        presets_raw = _load_yaml("weather_presets.yaml").get("presets") or {}
        if not isinstance(presets_raw, dict):
            raise RegistryError("weather_presets.yaml: 'presets' must be a mapping")
        weather_presets = {
            str(name): WeatherPresetRef(
                name=str(name),
                description=str((meta or {}).get("description", ""))
                if isinstance(meta, dict)
                else "",
            )
            for name, meta in presets_raw.items()
        }

        payloads_raw = _load_yaml("payloads.yaml").get("payloads") or {}
        if not isinstance(payloads_raw, dict):
            raise RegistryError("payloads.yaml: 'payloads' must be a mapping")

        return cls(
            airfields=airfields,
            aircraft=aircraft,
            theatres=theatres,
            weather_presets=weather_presets,
            payloads=payloads_raw,
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

    def payload_meta(self, name: str) -> Any:
        try:
            return self._payloads[name]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown payload '{name}'. Known: {sorted(self._payloads)}"
            ) from exc


@lru_cache(maxsize=1)
def get_channel_registry() -> ChannelRegistry:
    """Return the packaged Channel registry (loaded once)."""
    return ChannelRegistry.from_packaged_yaml()
