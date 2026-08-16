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
    with pytest.raises(RegistryError, match="Unknown airfield") as exc_info:
        registry.airdrome_id("NotARealAirfield")
    message = str(exc_info.value)
    assert "Manston" in message
    assert "BigginHill" in message


def test_thechannel_supported(registry):
    assert registry.has_theatre("TheChannel")
    assert "TheChannel" in registry.list_theatres()


def test_normandy_supported_and_needs_oar_point(registry):
    assert registry.has_theatre("Normandy")
    assert "Normandy" in registry.list_theatres()
    assert registry.airdrome_id("NeedsOarPoint") == 28
    assert registry.airfield_theatre("NeedsOarPoint") == "Normandy"
    assert registry.airfield_theatre("Manston") == "TheChannel"


def test_caucasus_supported_and_batumi(registry):
    assert registry.has_theatre("Caucasus")
    assert "Caucasus" in registry.list_theatres()
    assert registry.era_for_theatre("Caucasus") == "modern"
    assert registry.airdrome_id("Batumi", theatre="Caucasus") == 22
    assert registry.airfield_theatre("Batumi") == "Caucasus"
    assert registry.radio_mhz("Su-25T") == 251.0
    assert "Su-25T" in registry.known_aircraft(era="modern")
    assert "Su-25T" not in registry.known_aircraft(era="wwii")
    assert "Georgia" in registry.list_countries(era="modern")
    assert "Georgia" not in registry.list_countries(era="wwii")
    assert "Turkey" in registry.list_countries(era="modern")
    assert "Turkey" not in registry.list_countries(era="wwii")
    assert "USA" in registry.list_countries(era="modern")
    assert "USA" not in registry.list_countries(era="wwii")
    assert "UK" in registry.list_countries(era="modern")
    assert "UK" in registry.list_countries(era="wwii")
    assert "usaaf" not in registry.list_countries(era="modern")
    assert "usaaf" not in registry.list_countries(era="wwii")


def test_syria_supported_and_incirlik(registry):
    assert registry.has_theatre("Syria")
    assert "Syria" in registry.list_theatres()
    assert registry.era_for_theatre("Syria") == "modern"
    assert registry.airdrome_id("Incirlik", theatre="Syria") == 16
    assert registry.airfield_theatre("Incirlik") == "Syria"


def test_nevada_supported_and_nellis(registry):
    assert registry.has_theatre("Nevada")
    assert "Nevada" in registry.list_theatres()
    assert registry.era_for_theatre("Nevada") == "modern"
    assert registry.airdrome_id("Nellis", theatre="Nevada") == 4
    assert registry.airfield_theatre("Nellis") == "Nevada"


def test_falklands_supported_and_mount_pleasant(registry):
    assert registry.has_theatre("Falklands")
    assert "Falklands" in registry.list_theatres()
    assert registry.era_for_theatre("Falklands") == "modern"
    assert registry.airdrome_id("MountPleasant", theatre="Falklands") == 2
    assert registry.airfield_theatre("MountPleasant") == "Falklands"


def test_known_wwii_aircraft(registry):
    known = registry.known_aircraft()
    for aircraft_id in ("SpitfireLFMkIX", "Bf-109K-4", "FW-190A8", "FW-190D9"):
        assert aircraft_id in known


def test_sunny_clear_weather_preset(registry):
    preset = registry.weather_preset("sunny_clear")
    assert preset.name == "sunny_clear"


def test_dawn_and_marginal_weather_presets(registry):
    assert registry.weather_preset("dawn_clear").name == "dawn_clear"
    assert registry.weather_preset("marginal_vfr").name == "marginal_vfr"
    assert set(registry.list_weather_presets()) >= {
        "sunny_clear",
        "dawn_clear",
        "marginal_vfr",
    }
