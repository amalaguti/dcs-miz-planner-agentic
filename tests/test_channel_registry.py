"""Channel reference registry lookups (YAML-backed)."""

from __future__ import annotations

import pytest

from dcs_miz_planner.registry import RegistryError, get_channel_registry


@pytest.fixture
def registry():
    return get_channel_registry()


def test_manston_airdrome_id(registry):
    assert registry.airdrome_id("Manston") == 5


def test_spitfire_radio_mhz(registry):
    assert registry.radio_mhz("SpitfireLFMkIX") == 124.0
    assert registry.get_aircraft("SpitfireLFMkIX").radio_mhz == 124.0


def test_unknown_airfield_lists_known(registry):
    with pytest.raises(RegistryError, match="Unknown Channel airfield") as exc_info:
        registry.airdrome_id("NotARealAirfield")
    message = str(exc_info.value)
    assert "Manston" in message
    assert "BigginHill" in message


def test_thechannel_supported(registry):
    assert registry.has_theatre("TheChannel")
    assert "TheChannel" in registry.list_theatres()


def test_known_wwii_aircraft(registry):
    known = registry.known_aircraft()
    for aircraft_id in ("SpitfireLFMkIX", "Bf-109K-4", "FW-190A8", "FW-190D9"):
        assert aircraft_id in known


def test_sunny_clear_weather_preset(registry):
    preset = registry.weather_preset("sunny_clear")
    assert preset.name == "sunny_clear"
