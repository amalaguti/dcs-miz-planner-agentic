"""Theatre registry packages: per-theatre airfields + walker loader."""

from __future__ import annotations

import importlib
from importlib import resources

import pytest

from dcs_miz_planner.registry import RegistryError, get_channel_registry

_CHANNEL_AIRFIELDS = {
    "Abbeville": 1,
    "MervilleCalonne": 2,
    "SaintOmer": 3,
    "Dunkirk": 4,
    "Manston": 5,
    "Hawkinge": 6,
    "Lympne": 7,
    "Detling": 8,
    "Eastchurch": 10,
    "HighHalden": 12,
    "Headcorn": 13,
    "BigginHill": 14,
}

_CAUCASUS_AIRFIELDS = {
    "Batumi": 22,
    "Kobuleti": 24,
    "SenakiKolkhi": 23,
    "Kutaisi": 25,
    "TbilisiLochini": 29,
    "Vaziani": 31,
    "SochiAdler": 18,
    "Mozdok": 28,
}

_SYRIA_AIRFIELDS = {
    "Incirlik": 16,
}

_NEVADA_AIRFIELDS = {
    "Nellis": 4,
}

_FALKLANDS_AIRFIELDS = {
    "MountPleasant": 2,
}

_NORMANDY_AIRFIELDS = {
    "NeedsOarPoint": 28,
    "Chailey": 27,
    "Funtington": 29,
    "Tangmere": 30,
    "FordAF": 31,
    "Maupertus": 4,
    "SaintPierreduMont": 1,
    "Carpiquet": 19,
}


@pytest.fixture
def registry():
    return get_channel_registry()


def test_manston_on_thechannel(registry):
    assert registry.airdrome_id("Manston", theatre="TheChannel") == 5


def test_manston_on_normandy_fails(registry):
    with pytest.raises(RegistryError, match="Unknown airfield") as exc_info:
        registry.airdrome_id("Manston", theatre="Normandy")
    message = str(exc_info.value)
    assert "Manston" in message
    assert "NeedsOarPoint" in message


def test_needs_oar_point_on_thechannel_fails(registry):
    with pytest.raises(RegistryError, match="Unknown airfield") as exc_info:
        registry.airdrome_id("NeedsOarPoint", theatre="TheChannel")
    message = str(exc_info.value)
    assert "NeedsOarPoint" in message
    assert "Manston" in message


def test_needs_oar_point_on_normandy(registry):
    assert registry.airdrome_id("NeedsOarPoint", theatre="Normandy") == 28


def test_channel_airfields_exactly_verified_twelve(registry):
    names = registry.list_airfields(theatre="TheChannel")
    assert set(names) == set(_CHANNEL_AIRFIELDS)
    for name, aid in _CHANNEL_AIRFIELDS.items():
        assert registry.airdrome_id(name, theatre="TheChannel") == aid
    ids = {registry.airdrome_id(n, theatre="TheChannel") for n in names}
    assert 9 not in ids
    assert 11 not in ids


def test_caucasus_airfields_exactly_curated_eight(registry):
    names = registry.list_airfields(theatre="Caucasus")
    assert {n: registry.airdrome_id(n, theatre="Caucasus") for n in names} == _CAUCASUS_AIRFIELDS
    assert registry.airdrome_id("Batumi", theatre="Caucasus") == 22
    assert registry.airdrome_id("Mozdok", theatre="Caucasus") == 28
    assert registry.airdrome_id("NeedsOarPoint", theatre="Normandy") == 28
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Batumi", theatre="TheChannel")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Manston", theatre="Caucasus")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Mozdok", theatre="Normandy")


def test_syria_airfields_exactly_incirlik(registry):
    names = registry.list_airfields(theatre="Syria")
    assert {n: registry.airdrome_id(n, theatre="Syria") for n in names} == _SYRIA_AIRFIELDS
    assert registry.airdrome_id("Incirlik", theatre="Syria") == 16
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Incirlik", theatre="TheChannel")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Manston", theatre="Syria")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Batumi", theatre="Syria")


def test_nevada_airfields_exactly_nellis(registry):
    names = registry.list_airfields(theatre="Nevada")
    assert {n: registry.airdrome_id(n, theatre="Nevada") for n in names} == _NEVADA_AIRFIELDS
    assert registry.airdrome_id("Nellis", theatre="Nevada") == 4
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Nellis", theatre="TheChannel")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Manston", theatre="Nevada")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Incirlik", theatre="Nevada")


def test_falklands_airfields_exactly_mount_pleasant(registry):
    names = registry.list_airfields(theatre="Falklands")
    assert {n: registry.airdrome_id(n, theatre="Falklands") for n in names} == _FALKLANDS_AIRFIELDS
    assert registry.airdrome_id("MountPleasant", theatre="Falklands") == 2
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("MountPleasant", theatre="TheChannel")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Manston", theatre="Falklands")
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Nellis", theatre="Falklands")


def test_normandy_airfields_exactly_curated_eight(registry):
    names = registry.list_airfields(theatre="Normandy")
    assert {n: registry.airdrome_id(n, theatre="Normandy") for n in names} == _NORMANDY_AIRFIELDS
    assert registry.airdrome_id("Maupertus", theatre="Normandy") == 4
    with pytest.raises(RegistryError, match="Unknown airfield"):
        registry.airdrome_id("Maupertus", theatre="TheChannel")


def test_sunny_clear_without_normandy_weather_file(registry):
    preset = registry.weather_preset("sunny_clear")
    assert preset.name == "sunny_clear"
    normandy = resources.files("dcs_miz_planner.data") / "theatres" / "Normandy"
    assert not (normandy / "weather_presets.yaml").is_file()
    assert not (normandy / "weather_gallery.yaml").is_file()


def test_loader_has_no_data_channel_package():
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("dcs_miz_planner.data.channel")
