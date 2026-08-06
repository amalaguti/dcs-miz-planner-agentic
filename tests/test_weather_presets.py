"""Weather preset registry, validation, and compile coverage."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import channel_available_inventory

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.models import WeatherOpts
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.tools.surface import list_mission_options, validate_mission_spec
from dcs_miz_planner.validation import validate_mission_spec as validate_spec_model
from dcs_miz_planner.weather_invent import (
    ensure_weather_seed,
    resolve_weather_snapshot,
    snapshot_differs,
)

REPO = Path(__file__).resolve().parents[1]
DAWN = REPO / "examples" / "manston_dawn_freeflight.yaml"
MARGINAL = REPO / "examples" / "manston_marginal_vfr.yaml"
SUNNY = REPO / "examples" / "manston_cold_freeflight.yaml"
BROKEN = REPO / "examples" / "manston_broken_channel.yaml"
RAIN = REPO / "examples" / "manston_rain_overcast.yaml"


def test_registry_lists_weather_presets() -> None:
    names = get_channel_registry().list_weather_presets()
    assert set(names) >= {
        "sunny_clear",
        "dawn_clear",
        "marginal_vfr",
        "light_scattered_vfr",
        "high_scattered",
        "broken_channel",
        "overcast_low",
        "rain_overcast",
        "scattered_summer",
    }
    rain = get_channel_registry().weather_preset("rain_overcast")
    assert rain.cloud_preset == "RainyPreset1"
    assert set(rain.gallery_family) >= {"RainyPreset1", "RainyPreset2", "RainyPreset3"}
    broken = get_channel_registry().weather_preset("broken_channel")
    assert broken.gallery_family
    assert all(p.startswith("Preset") for p in broken.gallery_family)


def test_validate_dawn_and_marginal() -> None:
    inv = channel_available_inventory()
    assert validate_mission_spec(DAWN, inventory=inv)["ok"]
    assert validate_mission_spec(MARGINAL, inventory=inv)["ok"]


def test_list_mission_options_weather_supported(tmp_path: Path) -> None:
    from dcs_miz_planner.catalog import CatalogService

    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    result = list_mission_options(db_path=db)
    by_key = {(o["family"], o["id"]): o for o in result["options"]}
    assert by_key[("weather", "sunny_clear")]["support"] == "supported"
    assert by_key[("weather", "dawn_clear")]["support"] == "supported"
    assert by_key[("weather", "marginal_vfr")]["support"] == "supported"
    assert by_key[("weather", "broken_channel")]["support"] == "supported"
    assert by_key[("weather", "rain_overcast")]["support"] == "supported"
    assert set(result["weather_presets"]) >= {
        "sunny_clear",
        "dawn_clear",
        "marginal_vfr",
        "broken_channel",
        "rain_overcast",
    }


def _mission_weather_snippet(miz: Path) -> str:
    with zipfile.ZipFile(miz) as z:
        return z.read("mission").decode("utf-8")


def test_compile_weather_presets_differ(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    sunny = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(SUNNY), tmp_path / "sunny.miz", voice="raf"
    )
    dawn = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(DAWN), tmp_path / "dawn.miz", voice="raf"
    )
    marg = PyDCSCompiler(inventory=inv).compile(
        load_mission_spec(MARGINAL), tmp_path / "marg.miz", voice="raf"
    )
    sunny_m = _mission_weather_snippet(sunny)
    dawn_m = _mission_weather_snippet(dawn)
    marg_m = _mission_weather_snippet(marg)

    assert '["visibility"]' in sunny_m or "visibility" in sunny_m.lower()
    assert '["distance"]=80000' in sunny_m
    assert '["distance"]=45000' in dawn_m
    assert '["enable_fog"]=true' in dawn_m
    assert '["distance"]=6000' in marg_m
    assert '["density"]=8' in marg_m
    assert dawn_m != sunny_m
    assert marg_m != sunny_m


def test_compile_gallery_weather_presets(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    broken_spec = ensure_weather_seed(load_mission_spec(BROKEN), seed=42)
    rain_spec = ensure_weather_seed(load_mission_spec(RAIN), seed=42)
    broken = PyDCSCompiler(inventory=inv).compile(broken_spec, tmp_path / "broken.miz", voice="raf")
    rain = PyDCSCompiler(inventory=inv).compile(rain_spec, tmp_path / "rain.miz", voice="raf")
    broken_m = _mission_weather_snippet(broken)
    rain_m = _mission_weather_snippet(rain)
    assert '["preset"]=' in broken_m
    assert "Preset" in broken_m
    assert "RainyPreset" in rain_m
    assert validate_mission_spec(BROKEN, inventory=inv)["ok"]
    assert validate_mission_spec(RAIN, inventory=inv)["ok"]


def test_weather_invent_seed_determinism() -> None:
    base = load_mission_spec(BROKEN).model_copy(update={"weather_opts": None})
    a = resolve_weather_snapshot(ensure_weather_seed(base, seed=7))
    b = resolve_weather_snapshot(ensure_weather_seed(base, seed=7))
    c = resolve_weather_snapshot(ensure_weather_seed(base, seed=99))
    assert a.cloud_preset == b.cloud_preset
    assert a.temperature_c == b.temperature_c
    assert a.wind_ground is not None and b.wind_ground is not None
    assert a.wind_ground.speed_ms == b.wind_ground.speed_ms
    assert snapshot_differs(a, c)
    family = set(get_channel_registry().weather_preset("broken_channel").gallery_family)
    assert a.cloud_preset in family
    assert c.cloud_preset in family


def test_weather_invent_rain_stays_rainy_family() -> None:
    base = load_mission_spec(RAIN).model_copy(update={"weather_opts": None})
    for seed in (0, 1, 42, 99, 1000):
        snap = resolve_weather_snapshot(ensure_weather_seed(base, seed=seed))
        assert snap.cloud_preset is not None
        assert snap.cloud_preset.startswith("RainyPreset")


def test_weather_invent_sunny_no_gallery() -> None:
    base = load_mission_spec(SUNNY)
    snap = resolve_weather_snapshot(ensure_weather_seed(base, seed=42))
    assert snap.cloud_preset is None


def test_weather_opts_seed_loads() -> None:
    spec = load_mission_spec(BROKEN).model_copy(update={"weather_opts": WeatherOpts(seed=42)})
    assert spec.weather_opts is not None
    assert spec.weather_opts.seed == 42
    inv = channel_available_inventory()
    assert validate_spec_model(spec, inventory=inv).ok


def test_weather_sot_parity() -> None:
    from dcs_miz_planner.weather_sot import collect_weather_sot

    sets = collect_weather_sot()
    assert sets.enum, "WeatherPreset enum must not be empty"
    assert sets.aligned, (
        f"Weather SoT mismatch: enum={sorted(sets.enum)} yaml={sorted(sets.yaml)} "
        f"planning={sorted(sets.planning)} compiler={sorted(sets.compiler)}"
    )
