"""Compatibility façade over the Channel reference registry.

Prefer ``dcs_miz_planner.registry`` for new code. These names keep older imports working.
"""

from __future__ import annotations

from .registry import RegistryError, get_channel_registry

_registry = get_channel_registry()

CHANNEL_AIRDROME_IDS: dict[str, int] = {
    name: _registry.airdrome_id(name) for name in _registry.list_airfields()
}
KNOWN_AIRCRAFT: frozenset[str] = _registry.known_aircraft()
AIRCRAFT_RADIO_MHZ: dict[str, float] = {
    aircraft_id: _registry.radio_mhz(aircraft_id) for aircraft_id in _registry.list_aircraft()
}
SUPPORTED_THEATRES: frozenset[str] = frozenset(_registry.list_theatres())


def radio_frequency_mhz(aircraft: str) -> float:
    try:
        return _registry.radio_mhz(aircraft)
    except RegistryError as exc:
        raise KeyError(str(exc)) from exc


def airdrome_id(theatre: str, airfield_name: str) -> int:
    if not _registry.has_theatre(theatre):
        raise KeyError(f"Unsupported theatre for airfield lookup: {theatre}")
    try:
        return _registry.airdrome_id(airfield_name)
    except RegistryError as exc:
        raise KeyError(str(exc)) from exc
