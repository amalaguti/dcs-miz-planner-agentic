"""Slice 0b theatre-agnostic planning: fail-closed helpers, catalog tags, schema."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory, compile_needs_oar_point

from dcs_miz_planner.agent import PlanSession, plan_mission
from dcs_miz_planner.agent.immersion import host_normandy_combat_nudge
from dcs_miz_planner.agent.llm import (
    MANSTON_FREE_FLIGHT_JSON,
    NEEDS_OAR_POINT_FREE_FLIGHT_JSON,
    LLMResponse,
    StubLLM,
)
from dcs_miz_planner.agent.path_clamp import try_clamp_land_paths_if_needed
from dcs_miz_planner.agent.realism import date_realism_warnings
from dcs_miz_planner.agent.spec_schema import build_spec_schema
from dcs_miz_planner.allowlists import known_countries
from dcs_miz_planner.catalog import CatalogService
from dcs_miz_planner.channel_domain import (
    DOMAIN_THEATRES,
    DomainUnsupportedTheatre,
    airfield_relative_map_point,
    classify_domain_for_theatre,
    require_channel_domain,
    strike_domain_for_spec,
)
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.intercept_spawn import (
    INTERCEPT_SPAWN_RECIPES,
    intercept_spawn_for_theatre,
    intercept_supported,
)
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.registry import get_channel_registry
from dcs_miz_planner.reweather import ReweatherError, reweather_mission
from dcs_miz_planner.tools.surface import (
    get_mission_spec_schema,
    list_mission_options,
    list_strike_targets,
)
from dcs_miz_planner.validation import validate_mission_spec
from dcs_miz_planner.weather_invent import ensure_weather_seed, resolve_weather_snapshot
from dcs_miz_planner.weather_metar import format_synthetic_metar

REPO = Path(__file__).resolve().parents[1]
GA = REPO / "examples" / "manston_ground_attack.yaml"
NORMANDY_FF = REPO / "examples" / "needs_oar_point_cold_freeflight.yaml"
NORMANDY_CAP = REPO / "examples" / "needs_oar_point_cap.yaml"
NORMANDY_GA = REPO / "examples" / "needs_oar_point_ground_attack.yaml"
NORMANDY_INTERCEPT = REPO / "examples" / "needs_oar_point_dawn_intercept.yaml"
NORMANDY_ESCORT = REPO / "examples" / "needs_oar_point_escort.yaml"
NORMANDY_RECON = REPO / "examples" / "needs_oar_point_recon.yaml"
MANSTON_FF = REPO / "examples" / "manston_cold_freeflight.yaml"
CAUCASUS_FF = REPO / "examples" / "batumi_cold_freeflight.yaml"
CAUCASUS_CAP = REPO / "examples" / "batumi_black_sea_cap.yaml"
CAUCASUS_GA = REPO / "examples" / "batumi_kutaisi_ground_attack.yaml"
CAUCASUS_INTERCEPT = REPO / "examples" / "batumi_dawn_intercept.yaml"
CAUCASUS_ESCORT = REPO / "examples" / "batumi_black_sea_escort.yaml"
CAUCASUS_RECON = REPO / "examples" / "batumi_kutaisi_recon.yaml"
SYRIA_FF = REPO / "examples" / "incirlik_cold_freeflight.yaml"
SYRIA_CAP = REPO / "examples" / "incirlik_iskenderun_cap.yaml"
SYRIA_INTERCEPT = REPO / "examples" / "incirlik_dawn_intercept.yaml"
SYRIA_ESCORT = REPO / "examples" / "incirlik_iskenderun_escort.yaml"
SYRIA_GA = REPO / "examples" / "incirlik_aleppo_ground_attack.yaml"
SYRIA_RECON = REPO / "examples" / "incirlik_aleppo_recon.yaml"
NEVADA_FF = REPO / "examples" / "nellis_cold_freeflight.yaml"
NEVADA_CAP = REPO / "examples" / "nellis_north_range_cap.yaml"
NEVADA_INTERCEPT = REPO / "examples" / "nellis_dawn_intercept.yaml"
NEVADA_ESCORT = REPO / "examples" / "nellis_north_range_escort.yaml"
NEVADA_GA = REPO / "examples" / "nellis_creech_ground_attack.yaml"
NEVADA_RECON = REPO / "examples" / "nellis_creech_recon.yaml"
FALKLANDS_FF = REPO / "examples" / "mount_pleasant_cold_freeflight.yaml"
FALKLANDS_CAP = REPO / "examples" / "mount_pleasant_south_atlantic_cap.yaml"
FALKLANDS_INTERCEPT = REPO / "examples" / "mount_pleasant_dawn_intercept.yaml"
FALKLANDS_ESCORT = REPO / "examples" / "mount_pleasant_south_atlantic_escort.yaml"
FALKLANDS_GA = REPO / "examples" / "mount_pleasant_east_falkland_ground_attack.yaml"


def _inv():
    return channel_available_inventory()


def test_countries_uk_and_thirdreich_only() -> None:
    registry = get_channel_registry()
    countries = registry.list_countries(era="wwii")
    assert set(countries) == {"UK", "ThirdReich"}
    assert "Germany" not in countries
    assert "Georgia" not in countries
    assert known_countries(era="wwii") == frozenset({"UK", "ThirdReich"})
    assert "Georgia" in registry.list_countries()
    assert "Georgia" in known_countries()
    assert "Turkey" in registry.list_countries(era="modern")
    assert "Turkey" not in countries
    assert "USA" in registry.list_countries(era="modern")
    assert "USA" not in countries
    assert "usaaf" not in registry.list_countries()
    assert "Germany" not in registry.list_countries()
    assert "Germany" not in known_countries(era="modern")
    assert set(registry.list_countries(era="modern")) == {
        "Georgia",
        "Turkey",
        "USA",
        "UK",
        "Russia",
        "Syria",
        "Argentina",
    }
    assert "Chile" not in registry.list_countries(era="modern")
    assert "Chile" not in registry.list_countries()


def test_era_for_theatre_wwii() -> None:
    registry = get_channel_registry()
    assert registry.era_for_theatre("TheChannel") == "wwii"
    assert registry.era_for_theatre("Normandy") == "wwii"
    assert registry.era_for_theatre("Caucasus") == "modern"
    assert registry.era_for_theatre("Syria") == "modern"
    assert registry.era_for_theatre("Nevada") == "modern"
    assert registry.era_for_theatre("Falklands") == "modern"


def test_airfield_relative_map_point_passes_theatre() -> None:
    spec = load_mission_spec(NORMANDY_FF)
    x, y = airfield_relative_map_point(spec, bearing_deg=120.0, distance_km=5.0)
    assert isinstance(x, float)
    assert isinstance(y, float)


def test_falklands_strike_domain_classified() -> None:
    spec = load_mission_spec(FALKLANDS_GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"
    ff = load_mission_spec(FALKLANDS_FF)
    sea_x, sea_y = airfield_relative_map_point(ff, bearing_deg=150.0, distance_km=40.0)
    land_x, land_y = airfield_relative_map_point(ff, bearing_deg=269.0, distance_km=21.0)
    assert classify_domain_for_theatre("Falklands", sea_x, sea_y) == "sea"
    assert classify_domain_for_theatre("Falklands", land_x, land_y) == "land"
    assert (sea_x, sea_y) != (land_x, land_y)
    require_channel_domain("Falklands")


def test_domain_fail_closed_on_kola_strike() -> None:
    spec = load_mission_spec(GA).model_copy(update={"theatre": "Kola"})
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "domain_unsupported_theatre" for e in result.errors)
    with pytest.raises(DomainUnsupportedTheatre):
        require_channel_domain("Kola")
    with pytest.raises(DomainUnsupportedTheatre):
        strike_domain_for_spec(spec)


def test_nevada_strike_domain_classified() -> None:
    spec = load_mission_spec(NEVADA_GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"
    ff = load_mission_spec(NEVADA_FF)
    cap_x, cap_y = airfield_relative_map_point(ff, bearing_deg=350.0, distance_km=40.0)
    land_x, land_y = airfield_relative_map_point(ff, bearing_deg=303.0, distance_km=85.0)
    assert classify_domain_for_theatre("Nevada", cap_x, cap_y) == "land"
    assert classify_domain_for_theatre("Nevada", land_x, land_y) == "land"
    require_channel_domain("Nevada")


def test_syria_strike_domain_classified() -> None:
    spec = load_mission_spec(SYRIA_GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"
    ff = load_mission_spec(SYRIA_FF)
    sea_x, sea_y = airfield_relative_map_point(ff, bearing_deg=180.0, distance_km=40.0)
    land_x, land_y = airfield_relative_map_point(ff, bearing_deg=121.0, distance_km=200.0)
    adana_x, adana_y = airfield_relative_map_point(ff, bearing_deg=270.0, distance_km=40.0)
    assert classify_domain_for_theatre("Syria", sea_x, sea_y) == "sea"
    assert classify_domain_for_theatre("Syria", land_x, land_y) == "land"
    assert classify_domain_for_theatre("Syria", adana_x, adana_y) == "land"
    require_channel_domain("Syria")


def test_caucasus_strike_domain_classified() -> None:
    spec = load_mission_spec(CAUCASUS_GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"
    ff = load_mission_spec(CAUCASUS_FF)
    sea_x, sea_y = airfield_relative_map_point(ff, bearing_deg=270.0, distance_km=40.0)
    land_x, land_y = airfield_relative_map_point(ff, bearing_deg=43.0, distance_km=110.0)
    assert classify_domain_for_theatre("Caucasus", sea_x, sea_y) == "sea"
    assert classify_domain_for_theatre("Caucasus", land_x, land_y) == "land"
    require_channel_domain("Caucasus")


def test_normandy_strike_domain_classified() -> None:
    spec = load_mission_spec(NORMANDY_GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"
    ff = load_mission_spec(NORMANDY_FF)
    sea_x, sea_y = airfield_relative_map_point(ff, bearing_deg=180.0, distance_km=63.0)
    land_x, land_y = airfield_relative_map_point(ff, bearing_deg=180.0, distance_km=133.0)
    assert classify_domain_for_theatre("Normandy", sea_x, sea_y) == "sea"
    assert classify_domain_for_theatre("Normandy", land_x, land_y) == "land"
    require_channel_domain("Normandy")


def test_channel_strike_domain_still_classified() -> None:
    spec = load_mission_spec(GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"


def test_intercept_succeeds_on_normandy(tmp_path: Path) -> None:
    spec = load_mission_spec(NORMANDY_INTERCEPT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert intercept_supported("Normandy")
    recipe = intercept_spawn_for_theatre("Normandy")
    assert recipe.enemy_x == 78296.390625
    assert recipe.enemy_y == -84372.234375
    out = tmp_path / "normandy_intercept.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "78296.390625" in mission
        assert "30989.935547" not in mission


def test_intercept_succeeds_on_caucasus(tmp_path: Path) -> None:
    spec = load_mission_spec(CAUCASUS_INTERCEPT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert intercept_supported("Caucasus")
    recipe = intercept_spawn_for_theatre("Caucasus")
    assert recipe.enemy_x == -355810.6875
    assert recipe.enemy_y == 577386.1875
    out = tmp_path / "caucasus_intercept.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "-355810.6875" in mission
        assert "577386.1875" in mission
        assert "30989.935547" not in mission


def test_intercept_succeeds_on_syria(tmp_path: Path) -> None:
    spec = load_mission_spec(SYRIA_INTERCEPT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert intercept_supported("Syria")
    recipe = intercept_spawn_for_theatre("Syria")
    assert recipe.enemy_x == 181207.773438
    assert recipe.enemy_y == -35240.347656
    out = tmp_path / "syria_intercept.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "181207.773438" in mission
        assert "-35240.347656" in mission
        assert "30989.935547" not in mission


def test_intercept_succeeds_on_nevada(tmp_path: Path) -> None:
    spec = load_mission_spec(NEVADA_INTERCEPT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert intercept_supported("Nevada")
    recipe = intercept_spawn_for_theatre("Nevada")
    assert recipe.anchor_x == -398195.375
    assert recipe.anchor_y == -17233.236816
    assert recipe.offset_x == 39392.31012048834
    assert recipe.offset_y == -6945.927106677216
    assert recipe.enemy_x == -358803.06487951166
    assert recipe.enemy_y == pytest.approx(-24179.163922677217)
    out = tmp_path / "nevada_intercept.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "-358803.06487951166" in mission
        assert "30989.935547" not in mission
        assert "181207.773438" not in mission


def test_intercept_succeeds_on_falklands(tmp_path: Path) -> None:
    spec = load_mission_spec(FALKLANDS_INTERCEPT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert intercept_supported("Falklands")
    recipe = intercept_spawn_for_theatre("Falklands")
    assert recipe.anchor_x == 73318.320312
    assert recipe.anchor_y == 47168.748047
    assert recipe.offset_x == -34641.016151377546
    assert recipe.offset_y == 20000.0
    assert recipe.enemy_x == 38677.30416062245
    assert recipe.enemy_y == 67168.748047
    out = tmp_path / "falklands_intercept.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "38677.30416062245" in mission
        assert "67168.748047" in mission
        assert "30989.935547" not in mission
        assert "-358803.06487951166" not in mission
        assert "181207.773438" not in mission


def test_intercept_unsupported_hint_lists_recipe_keys() -> None:
    spec = load_mission_spec(FALKLANDS_INTERCEPT).model_copy(update={"theatre": "Kola"})
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    err = next(e for e in result.errors if e.code == "intercept_unsupported_theatre")
    hint = err.hint or ""
    for key in INTERCEPT_SPAWN_RECIPES:
        assert key in hint
    assert "TheChannel, Normandy, or Caucasus" not in hint


def test_domain_unsupported_hint_lists_supported_theatres() -> None:
    spec = load_mission_spec(GA).model_copy(update={"theatre": "Kola"})
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    err = next(e for e in result.errors if e.code == "domain_unsupported_theatre")
    hint = err.hint or ""
    for key in DOMAIN_THEATRES:
        assert key in hint
    assert "Nevada" in hint
    assert "Falklands" in hint
    assert "TheChannel, Normandy, Caucasus, or Syria" not in hint


def test_escort_succeeds_on_normandy(tmp_path: Path) -> None:
    spec = load_mission_spec(NORMANDY_ESCORT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "normandy_escort.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "MosquitoFBMkVI" in mission
        assert '["task"]="Escort"' in mission


def test_escort_succeeds_on_caucasus(tmp_path: Path) -> None:
    spec = load_mission_spec(CAUCASUS_ESCORT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "caucasus_escort.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert '["type"]="Su-25T"' in mission
        assert '["task"]="Escort"' in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "30989.935547" not in mission
        assert "78296.390625" not in mission


def test_escort_succeeds_on_syria(tmp_path: Path) -> None:
    spec = load_mission_spec(SYRIA_ESCORT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "syria_escort.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert '["type"]="Su-25T"' in mission
        assert '["task"]="Escort"' in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "30989.935547" not in mission
        assert "-35402.577148" not in mission


def test_escort_succeeds_on_nevada(tmp_path: Path) -> None:
    spec = load_mission_spec(NEVADA_ESCORT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "nevada_escort.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert '["type"]="Su-25T"' in mission
        assert '["task"]="Escort"' in mission
        assert "USA" in mission
        assert "Russia" in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "ThirdReich" not in mission
        assert "30989.935547" not in mission
        assert "181207.773438" not in mission


def test_escort_succeeds_on_falklands(tmp_path: Path) -> None:
    spec = load_mission_spec(FALKLANDS_ESCORT)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "falklands_escort.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert '["type"]="Su-25T"' in mission
        assert '["task"]="Escort"' in mission
        assert "UK" in mission
        assert "Argentina" in mission
        assert "MosquitoFBMkVI" not in mission
        assert "Bf-109K-4" not in mission
        assert "ThirdReich" not in mission
        assert "30989.935547" not in mission
        assert "-358803.06487951166" not in mission
        assert "181207.773438" not in mission


def test_recon_succeeds_on_normandy(tmp_path: Path) -> None:
    spec = load_mission_spec(NORMANDY_RECON)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "normandy_recon.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "Reconnaissance" in mission
        assert "Blitz_36-6700A" in mission


def test_recon_succeeds_on_caucasus(tmp_path: Path) -> None:
    spec = load_mission_spec(CAUCASUS_RECON)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    out = tmp_path / "caucasus_recon.miz"
    PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert out.is_file()
    with zipfile.ZipFile(out) as zf:
        mission = zf.read("mission").decode("utf-8")
        assert "Reconnaissance" in mission
        assert "Ural-375" in mission
        assert "Blitz_36-6700A" not in mission
        assert "30989.935547" not in mission


def test_channel_intercept_recipe_literals() -> None:
    recipe = intercept_spawn_for_theatre("TheChannel")
    assert recipe.hawkinge_x == 26989.935547
    assert recipe.hawkinge_y == -29402.577148
    assert recipe.dover_offset_x == 4000.0
    assert recipe.dover_offset_y == -6000.0
    assert recipe.enemy_x == 30989.935547
    assert recipe.enemy_y == -35402.577148


def test_path_clamp_skipped_on_normandy() -> None:
    spec = load_mission_spec(GA).model_copy(
        update={"theatre": "Normandy", "player": load_mission_spec(NORMANDY_FF).player}
    )
    assert try_clamp_land_paths_if_needed(spec) is None


def test_channel_place_tagged_thechannel() -> None:
    registry = get_channel_registry()
    places = [o for o in registry.list_planning_options() if o.family == "channel_place"]
    assert places
    belt = next(o for o in places if o.id == "french_coast_strike_belt")
    assert belt.meta.get("theatre") == "TheChannel"
    home = next(o for o in places if o.id == "needs_oar_point_home")
    cap = next(o for o in places if o.id == "cherbourg_channel_cap")
    assert home.meta.get("theatre") == "Normandy"
    assert cap.meta.get("theatre") == "Normandy"
    assert cap.meta.get("cap_bearing_deg") == 180
    assert cap.meta.get("cap_distance_km") == 63
    assert "intercept" in cap.meta.get("mission_types", [])
    assert "escort" in cap.meta.get("mission_types", [])
    inland = next(o for o in places if o.id == "maupertus_inland_strike")
    assert inland.meta.get("theatre") == "Normandy"
    assert inland.meta.get("domain") == "land"
    batumi_home = next(o for o in places if o.id == "batumi_home")
    assert batumi_home.meta.get("theatre") == "Caucasus"
    assert "ground_attack" in batumi_home.meta.get("mission_types", [])
    assert "intercept" in batumi_home.meta.get("mission_types", [])
    assert "escort" in batumi_home.meta.get("mission_types", [])
    assert "recon" in batumi_home.meta.get("mission_types", [])
    batumi_cap = next(o for o in places if o.id == "batumi_black_sea_cap")
    assert batumi_cap.meta.get("theatre") == "Caucasus"
    assert batumi_cap.meta.get("cap_bearing_deg") == 270
    assert batumi_cap.meta.get("cap_distance_km") == 40
    assert "intercept" in batumi_cap.meta.get("mission_types", [])
    assert "escort" in batumi_cap.meta.get("mission_types", [])
    kutaisi = next(o for o in places if o.id == "kutaisi_inland_strike")
    assert kutaisi.meta.get("theatre") == "Caucasus"
    assert kutaisi.meta.get("domain") == "land"
    assert kutaisi.meta.get("strike_bearing_deg") == 43
    assert kutaisi.meta.get("strike_distance_km") == 110
    assert "escort" not in kutaisi.meta.get("mission_types", [])
    assert "recon" in kutaisi.meta.get("mission_types", [])
    incirlik_home = next(o for o in places if o.id == "incirlik_home")
    assert incirlik_home.meta.get("theatre") == "Syria"
    assert "cap" in incirlik_home.meta.get("mission_types", [])
    assert "intercept" in incirlik_home.meta.get("mission_types", [])
    assert "escort" in incirlik_home.meta.get("mission_types", [])
    assert "ground_attack" in incirlik_home.meta.get("mission_types", [])
    assert "recon" in incirlik_home.meta.get("mission_types", [])
    incirlik_cap = next(o for o in places if o.id == "incirlik_iskenderun_cap")
    assert incirlik_cap.meta.get("theatre") == "Syria"
    assert incirlik_cap.meta.get("cap_bearing_deg") == 180
    assert incirlik_cap.meta.get("cap_distance_km") == 40
    assert incirlik_cap.meta.get("cap_distance_km") != 63
    assert incirlik_cap.meta.get("cap_bearing_deg") != 270
    assert "intercept" in incirlik_cap.meta.get("mission_types", [])
    assert "escort" in incirlik_cap.meta.get("mission_types", [])
    assert "ground_attack" not in incirlik_cap.meta.get("mission_types", [])
    assert "recon" not in incirlik_cap.meta.get("mission_types", [])
    aleppo = next(o for o in places if o.id == "aleppo_inland_strike")
    assert aleppo.meta.get("theatre") == "Syria"
    assert aleppo.meta.get("domain") == "land"
    assert aleppo.meta.get("strike_bearing_deg") == 121
    assert aleppo.meta.get("strike_distance_km") == 200
    assert "ground_attack" in aleppo.meta.get("mission_types", [])
    assert "recon" in aleppo.meta.get("mission_types", [])
    assert "escort" not in aleppo.meta.get("mission_types", [])
    nellis_home = next(o for o in places if o.id == "nellis_home")
    assert nellis_home.meta.get("theatre") == "Nevada"
    assert "cap" in nellis_home.meta.get("mission_types", [])
    assert "free_flight" in nellis_home.meta.get("mission_types", [])
    assert "intercept" in nellis_home.meta.get("mission_types", [])
    assert "escort" in nellis_home.meta.get("mission_types", [])
    assert "ground_attack" in nellis_home.meta.get("mission_types", [])
    assert "recon" in nellis_home.meta.get("mission_types", [])
    nellis_cap = next(o for o in places if o.id == "nellis_north_range_cap")
    assert nellis_cap.meta.get("theatre") == "Nevada"
    assert nellis_cap.meta.get("domain") == "land"
    assert nellis_cap.meta.get("cap_bearing_deg") == 350
    assert nellis_cap.meta.get("cap_distance_km") == 40
    assert nellis_cap.meta.get("cap_altitude_m") == 4000
    assert nellis_cap.meta.get("cap_bearing_deg") != 180
    assert nellis_cap.meta.get("cap_bearing_deg") != 270
    assert "cap" in nellis_cap.meta.get("mission_types", [])
    assert "intercept" in nellis_cap.meta.get("mission_types", [])
    assert "escort" in nellis_cap.meta.get("mission_types", [])
    assert "ground_attack" not in nellis_cap.meta.get("mission_types", [])
    assert "recon" not in nellis_cap.meta.get("mission_types", [])
    creech = next(o for o in places if o.id == "creech_range_strike")
    assert creech.meta.get("theatre") == "Nevada"
    assert creech.meta.get("domain") == "land"
    assert creech.meta.get("strike_bearing_deg") == 303
    assert creech.meta.get("strike_distance_km") == 85
    assert "ground_attack" in creech.meta.get("mission_types", [])
    assert "recon" in creech.meta.get("mission_types", [])
    assert "escort" not in creech.meta.get("mission_types", [])
    mp_home = next(o for o in places if o.id == "mount_pleasant_home")
    assert mp_home.meta.get("theatre") == "Falklands"
    assert "cap" in mp_home.meta.get("mission_types", [])
    assert "free_flight" in mp_home.meta.get("mission_types", [])
    assert "intercept" in mp_home.meta.get("mission_types", [])
    assert "escort" in mp_home.meta.get("mission_types", [])
    assert "ground_attack" in mp_home.meta.get("mission_types", [])
    assert "recon" not in mp_home.meta.get("mission_types", [])
    mp_cap = next(o for o in places if o.id == "mount_pleasant_south_atlantic_cap")
    assert mp_cap.meta.get("theatre") == "Falklands"
    assert mp_cap.meta.get("domain") == "sea"
    assert mp_cap.meta.get("cap_bearing_deg") == 150
    assert mp_cap.meta.get("cap_distance_km") == 40
    assert mp_cap.meta.get("cap_altitude_m") == 4000
    assert mp_cap.meta.get("cap_bearing_deg") != 350
    assert mp_cap.meta.get("cap_bearing_deg") != 180
    assert mp_cap.meta.get("cap_bearing_deg") != 270
    assert mp_cap.meta.get("cap_distance_km") != 25
    assert mp_cap.meta.get("cap_distance_km") != 63
    assert "cap" in mp_cap.meta.get("mission_types", [])
    assert "intercept" in mp_cap.meta.get("mission_types", [])
    assert "escort" in mp_cap.meta.get("mission_types", [])
    assert "ground_attack" not in mp_cap.meta.get("mission_types", [])
    assert "recon" not in mp_cap.meta.get("mission_types", [])
    east_fk = next(o for o in places if o.id == "east_falkland_inland_strike")
    assert east_fk.meta.get("theatre") == "Falklands"
    assert east_fk.meta.get("domain") == "land"
    assert east_fk.meta.get("strike_bearing_deg") == 269
    assert east_fk.meta.get("strike_distance_km") == 21
    assert "ground_attack" in east_fk.meta.get("mission_types", [])
    assert "recon" not in east_fk.meta.get("mission_types", [])
    assert "cap" not in east_fk.meta.get("mission_types", [])
    assert inland.meta.get("strike_bearing_deg") == 180
    assert inland.meta.get("strike_distance_km") == 133
    assert "recon" in inland.meta.get("mission_types", [])
    for opt in places:
        if opt.id in {
            "needs_oar_point_home",
            "cherbourg_channel_cap",
            "maupertus_inland_strike",
        }:
            assert opt.meta.get("theatre") == "Normandy"
        elif opt.id in {"batumi_home", "batumi_black_sea_cap", "kutaisi_inland_strike"}:
            assert opt.meta.get("theatre") == "Caucasus"
        elif opt.id in {"incirlik_home", "incirlik_iskenderun_cap", "aleppo_inland_strike"}:
            assert opt.meta.get("theatre") == "Syria"
        elif opt.id in {"nellis_home", "nellis_north_range_cap", "creech_range_strike"}:
            assert opt.meta.get("theatre") == "Nevada"
        elif opt.id in {
            "mount_pleasant_home",
            "mount_pleasant_south_atlantic_cap",
            "east_falkland_inland_strike",
        }:
            assert opt.meta.get("theatre") == "Falklands"
        else:
            assert opt.meta.get("theatre") == "TheChannel"


def test_schema_theatre_caucasus_free_flight() -> None:
    view = build_spec_schema("free_flight", theatre="Caucasus")
    assert view.example["theatre"] == "Caucasus"
    assert view.example["player"]["airfield"] == "Batumi"
    assert view.example["player"]["aircraft"] == "Su-25T"
    assert view.example["player"]["country"] == "Georgia"
    assert view.example["player"]["airfield"] != "Manston"
    assert view.example["player"]["airfield"] != "NeedsOarPoint"
    tool = get_mission_spec_schema("free_flight", theatre="Caucasus")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "Batumi"
    blob = " ".join(view.notes)
    assert "Batumi" in blob
    assert "Su-25T" in blob
    assert "Georgia" in blob
    assert "batumi_cold_freeflight.yaml" in blob
    assert "manston_" not in blob.lower()
    assert "examples are Channel templates" not in blob
    assert "SpitfireLFMkIX" not in blob
    assert "ENG0_MAGNETO0" not in blob
    assert "channel_place" not in blob
    assert "NeedsOarPoint" not in blob
    assert "french_coast" not in blob


def test_schema_theatre_syria_free_flight() -> None:
    view = build_spec_schema("free_flight", theatre="Syria")
    assert view.example["theatre"] == "Syria"
    assert view.example["player"]["airfield"] == "Incirlik"
    assert view.example["player"]["aircraft"] == "Su-25T"
    assert view.example["player"]["country"] == "Turkey"
    assert view.example["player"]["airfield"] != "Manston"
    assert view.example["player"]["airfield"] != "NeedsOarPoint"
    assert view.example["player"]["airfield"] != "Batumi"
    tool = get_mission_spec_schema("free_flight", theatre="Syria")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "Incirlik"
    blob = " ".join(view.notes)
    assert "Incirlik" in blob
    assert "Su-25T" in blob
    assert "Turkey" in blob
    assert "incirlik_cold_freeflight.yaml" in blob
    assert "manston_" not in blob.lower()
    assert "examples are Channel templates" not in blob
    assert "SpitfireLFMkIX" not in blob
    assert "ENG0_MAGNETO0" not in blob
    assert "channel_place" not in blob
    assert "NeedsOarPoint" not in blob
    assert "Batumi" not in blob
    assert "french_coast" not in blob


def test_schema_theatre_nevada_free_flight() -> None:
    view = build_spec_schema("free_flight", theatre="Nevada")
    assert view.example["theatre"] == "Nevada"
    assert view.example["player"]["airfield"] == "Nellis"
    assert view.example["player"]["aircraft"] == "Su-25T"
    assert view.example["player"]["country"] == "USA"
    assert view.example["player"]["airfield"] != "Manston"
    assert view.example["player"]["airfield"] != "NeedsOarPoint"
    assert view.example["player"]["airfield"] != "Batumi"
    assert view.example["player"]["airfield"] != "Incirlik"
    assert view.example["player"]["airfield"] != "GroomLake"
    tool = get_mission_spec_schema("free_flight", theatre="Nevada")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "Nellis"
    blob = " ".join(view.notes)
    assert "Nellis" in blob
    assert "Su-25T" in blob
    assert "USA" in blob
    assert "nellis_cold_freeflight.yaml" in blob
    assert "groom_lake_cold_freeflight.yaml" not in blob
    assert "manston_" not in blob.lower()
    assert "examples are Channel templates" not in blob
    assert "SpitfireLFMkIX" not in blob
    assert "ENG0_MAGNETO0" not in blob
    assert "channel_place" not in blob
    assert "NeedsOarPoint" not in blob
    assert "Batumi" not in blob
    assert "Incirlik" not in blob
    assert "french_coast" not in blob


def test_schema_theatre_falklands_free_flight() -> None:
    view = build_spec_schema("free_flight", theatre="Falklands")
    assert view.example["theatre"] == "Falklands"
    assert view.example["player"]["airfield"] == "MountPleasant"
    assert view.example["player"]["aircraft"] == "Su-25T"
    assert view.example["player"]["country"] == "UK"
    assert view.example["player"]["airfield"] != "Manston"
    assert view.example["player"]["airfield"] != "NeedsOarPoint"
    assert view.example["player"]["airfield"] != "Batumi"
    assert view.example["player"]["airfield"] != "Incirlik"
    assert view.example["player"]["airfield"] != "Nellis"
    tool = get_mission_spec_schema("free_flight", theatre="Falklands")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "MountPleasant"
    blob = " ".join(view.notes)
    assert "MountPleasant" in blob or "Mount Pleasant" in blob
    assert "Su-25T" in blob
    assert "UK" in blob
    assert "mount_pleasant_cold_freeflight.yaml" in blob
    assert "rio_gallegos_cold_freeflight.yaml" not in blob
    assert view.example["player"]["airfield"] != "RioGallegos"
    assert view.example["player"]["airfield"] != "PortStanley"
    assert "manston_" not in blob.lower()
    assert "examples are Channel templates" not in blob
    assert "SpitfireLFMkIX" not in blob
    assert "ENG0_MAGNETO0" not in blob
    assert "channel_place" not in blob
    assert "NeedsOarPoint" not in blob
    assert "Batumi" not in blob
    assert "Incirlik" not in blob
    assert "Nellis" not in blob
    assert "french_coast" not in blob


def test_schema_theatre_syria_combat_no_manston_skeleton() -> None:
    ga = build_spec_schema("ground_attack", theatre="Syria")
    assert ga.example["theatre"] == "Syria"
    assert ga.example["player"]["airfield"] == "Incirlik"
    assert ga.example["player"]["aircraft"] == "Su-25T"
    assert ga.example["player"]["payload"] == "su25t_2x_fab250"
    assert ga.example["strike"]["bearing_deg"] == 121
    assert ga.example["strike"]["distance_km"] == 200
    assert ga.example["targets"][0]["unit"] == "Ural-375"
    assert ga.example["targets"][0]["country"] == "Syria"
    ga_blob = " ".join(ga.notes)
    assert "aleppo_inland_strike" in ga_blob or "Aleppo" in ga_blob
    assert "incirlik_aleppo_ground_attack.yaml" in ga_blob
    assert "french_coast" not in ga_blob
    assert "manston_" not in ga_blob.lower()
    assert "kutaisi_inland_strike" not in ga_blob
    cap = build_spec_schema("cap", theatre="Syria")
    assert cap.example["theatre"] == "Syria"
    assert cap.example["player"]["airfield"] == "Incirlik"
    assert cap.example["player"]["aircraft"] == "Su-25T"
    assert cap.example["player"]["country"] == "Turkey"
    assert cap.example["cap"]["bearing_deg"] == 180
    assert cap.example["cap"]["distance_km"] == 40
    assert cap.example["cap"]["distance_km"] != 63
    assert cap.example["cap"]["bearing_deg"] != 270
    assert cap.example["enemies"][0]["country"] == "Syria"
    cap_blob = " ".join(cap.notes)
    assert "incirlik_iskenderun_cap.yaml" in cap_blob
    assert "manston_" not in cap_blob.lower()
    assert "NeedsOarPoint" not in cap_blob
    assert "Batumi" not in cap_blob
    assert "french_coast" not in cap_blob
    tool = get_mission_spec_schema("cap", theatre="Syria")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "Incirlik"
    intercept = build_spec_schema("intercept", theatre="Syria")
    assert intercept.example["theatre"] == "Syria"
    assert intercept.example["player"]["airfield"] == "Incirlik"
    assert intercept.example["enemies"][0]["country"] == "Syria"
    intercept_blob = " ".join(intercept.notes)
    assert "incirlik_dawn_intercept.yaml" in intercept_blob
    assert "manston_" not in intercept_blob.lower()
    assert "NeedsOarPoint" not in intercept_blob
    assert "Batumi" not in intercept_blob
    intercept_tool = get_mission_spec_schema("intercept", theatre="Syria")
    assert intercept_tool["ok"] is True
    assert intercept_tool["example"]["player"]["airfield"] == "Incirlik"
    escort = get_mission_spec_schema("escort", theatre="Syria")
    assert escort["ok"] is True
    assert escort["example"]["theatre"] == "Syria"
    assert escort["example"]["player"]["airfield"] == "Incirlik"
    assert escort["example"]["player"]["aircraft"] == "Su-25T"
    assert escort["example"]["package"][0]["aircraft"] == "Su-25T"
    assert escort["example"]["package"][0]["country"] == "Turkey"
    assert escort["example"]["enemies"][0]["country"] == "Syria"
    assert escort["example"]["escort"]["bearing_deg"] == 180
    assert escort["example"]["escort"]["distance_km"] == 40
    assert escort["example"]["escort"]["distance_km"] != 63
    assert escort["example"]["escort"]["bearing_deg"] != 270
    assert escort["example"]["player"]["airfield"] != "Manston"
    assert escort["example"]["player"]["airfield"] != "Batumi"
    assert escort["example"]["player"]["airfield"] != "NeedsOarPoint"
    escort_blob = json.dumps({k: v for k, v in escort["example"].items() if k != "description"})
    assert "MosquitoFBMkVI" not in escort_blob
    assert "Bf-109K-4" not in escort_blob
    escort_notes = " ".join(build_spec_schema("escort", theatre="Syria").notes)
    assert "incirlik_iskenderun_escort.yaml" in escort_notes
    assert "manston_" not in escort_notes.lower()
    ga_tool = get_mission_spec_schema("ground_attack", theatre="Syria")
    assert ga_tool["ok"] is True
    assert ga_tool["example"]["player"]["airfield"] == "Incirlik"
    assert ga_tool["example"]["strike"]["bearing_deg"] == 121
    assert ga_tool["example"]["strike"]["distance_km"] == 200
    assert ga_tool["example"]["targets"][0]["country"] == "Syria"
    recon_tool = get_mission_spec_schema("recon", theatre="Syria")
    assert recon_tool["ok"] is True
    assert recon_tool["example"]["theatre"] == "Syria"
    assert recon_tool["example"]["player"]["airfield"] == "Incirlik"
    assert recon_tool["example"]["player"]["aircraft"] == "Su-25T"
    assert recon_tool["example"]["recon"]["bearing_deg"] == 121
    assert recon_tool["example"]["recon"]["distance_km"] == 200
    assert recon_tool["example"]["recon"]["distance_km"] != 40
    assert recon_tool["example"]["recon"]["bearing_deg"] != 180
    assert recon_tool["example"]["targets"][0]["unit"] == "Ural-375"
    assert recon_tool["example"]["targets"][0]["country"] == "Syria"
    assert recon_tool["example"]["player"]["airfield"] != "Manston"
    assert recon_tool["example"]["player"]["airfield"] != "Batumi"
    assert recon_tool["example"]["player"]["airfield"] != "NeedsOarPoint"
    assert not recon_tool["example"]["player"].get("payload")
    recon_notes = " ".join(build_spec_schema("recon", theatre="Syria").notes)
    assert "aleppo_inland_strike" in recon_notes or "Aleppo" in recon_notes
    assert "incirlik_aleppo_recon.yaml" in recon_notes
    assert "french_coast" not in recon_notes
    assert "manston_" not in recon_notes.lower()
    assert "kutaisi_inland_strike" not in recon_notes


def test_schema_theatre_nevada_combat_no_manston_skeleton() -> None:
    ga = build_spec_schema("ground_attack", theatre="Nevada")
    assert ga.example["theatre"] == "Nevada"
    assert ga.example["player"]["airfield"] == "Nellis"
    assert ga.example["player"]["aircraft"] == "Su-25T"
    assert ga.example["player"]["country"] == "USA"
    assert ga.example["player"]["payload"] == "su25t_2x_fab250"
    assert ga.example["strike"]["bearing_deg"] == 303
    assert ga.example["strike"]["distance_km"] == 85
    assert ga.example["strike"]["altitude_m"] == 2000
    assert ga.example["strike"]["bearing_deg"] != 350
    assert ga.example["strike"]["distance_km"] != 40
    assert ga.example["targets"][0]["unit"] == "Ural-375"
    assert ga.example["targets"][0]["country"] == "Russia"
    assert ga.example["player"]["airfield"] != "Manston"
    assert ga.example["player"]["airfield"] != "Incirlik"
    assert ga.example["player"]["airfield"] != "Batumi"
    ga_blob = " ".join(ga.notes)
    assert "creech_range_strike" in ga_blob or "Creech" in ga_blob
    assert "nellis_creech_ground_attack.yaml" in ga_blob
    assert "french_coast" not in ga_blob
    assert "manston_" not in ga_blob.lower()
    ga_tool = get_mission_spec_schema("ground_attack", theatre="Nevada")
    assert ga_tool["ok"] is True
    assert ga_tool["example"]["player"]["airfield"] == "Nellis"
    assert ga_tool["example"]["strike"]["bearing_deg"] == 303
    assert ga_tool["example"]["targets"][0]["country"] == "Russia"
    recon = build_spec_schema("recon", theatre="Nevada")
    assert recon.example["theatre"] == "Nevada"
    assert recon.example["player"]["airfield"] == "Nellis"
    assert recon.example["player"]["aircraft"] == "Su-25T"
    assert recon.example["player"]["country"] == "USA"
    assert recon.example["recon"]["bearing_deg"] == 303
    assert recon.example["recon"]["distance_km"] == 85
    assert recon.example["recon"]["altitude_m"] == 2000
    assert recon.example["recon"]["distance_km"] != 40
    assert recon.example["recon"]["bearing_deg"] != 350
    assert recon.example["targets"][0]["unit"] == "Ural-375"
    assert recon.example["targets"][0]["country"] == "Russia"
    assert recon.example["player"]["airfield"] != "Manston"
    assert recon.example["player"]["airfield"] != "Incirlik"
    assert recon.example["player"]["airfield"] != "Batumi"
    assert not recon.example["player"].get("payload")
    recon_blob = " ".join(recon.notes)
    assert "creech_range_strike" in recon_blob or "Creech" in recon_blob
    assert "nellis_creech_recon.yaml" in recon_blob
    assert "french_coast" not in recon_blob
    assert "manston_" not in recon_blob.lower()
    recon_tool = get_mission_spec_schema("recon", theatre="Nevada")
    assert recon_tool["ok"] is True
    assert recon_tool["example"]["player"]["airfield"] == "Nellis"
    assert recon_tool["example"]["recon"]["bearing_deg"] == 303
    assert recon_tool["example"]["targets"][0]["country"] == "Russia"
    assert not recon_tool["example"]["player"].get("payload")
    escort = build_spec_schema("escort", theatre="Nevada")
    assert escort.example["theatre"] == "Nevada"
    assert escort.example["player"]["airfield"] == "Nellis"
    assert escort.example["player"]["aircraft"] == "Su-25T"
    assert escort.example["player"]["country"] == "USA"
    assert escort.example["package"][0]["aircraft"] == "Su-25T"
    assert escort.example["package"][0]["country"] == "USA"
    assert escort.example["enemies"][0]["country"] == "Russia"
    assert escort.example["escort"]["bearing_deg"] == 350
    assert escort.example["escort"]["distance_km"] == 40
    assert escort.example["escort"]["altitude_m"] == 4000
    assert escort.example["escort"]["bearing_deg"] != 180
    assert escort.example["escort"]["bearing_deg"] != 270
    assert escort.example["escort"]["distance_km"] != 55
    assert escort.example["escort"]["distance_km"] != 63
    assert escort.example["player"]["airfield"] != "Manston"
    assert escort.example["player"]["airfield"] != "Incirlik"
    assert escort.example["player"]["airfield"] != "Batumi"
    escort_blob = " ".join(escort.notes)
    assert "nellis_north_range_escort.yaml" in escort_blob
    assert "manston_" not in escort_blob.lower()
    assert "NeedsOarPoint" not in escort_blob
    assert "french_coast" not in escort_blob
    escort_tool = get_mission_spec_schema("escort", theatre="Nevada")
    assert escort_tool["ok"] is True
    assert escort_tool["example"]["player"]["airfield"] == "Nellis"
    assert escort_tool["example"]["package"][0]["country"] == "USA"
    assert escort_tool["example"]["enemies"][0]["country"] == "Russia"
    assert escort_tool["example"]["escort"]["bearing_deg"] == 350
    intercept = build_spec_schema("intercept", theatre="Nevada")
    assert intercept.example["theatre"] == "Nevada"
    assert intercept.example["player"]["airfield"] == "Nellis"
    assert intercept.example["player"]["aircraft"] == "Su-25T"
    assert intercept.example["player"]["country"] == "USA"
    assert intercept.example["enemies"][0]["country"] == "Russia"
    assert intercept.example["player"]["airfield"] != "Manston"
    assert intercept.example["player"]["airfield"] != "Incirlik"
    assert intercept.example["player"]["airfield"] != "Batumi"
    intercept_blob = " ".join(intercept.notes)
    assert "nellis_dawn_intercept.yaml" in intercept_blob
    assert "manston_" not in intercept_blob.lower()
    assert "NeedsOarPoint" not in intercept_blob
    assert "Batumi" not in intercept_blob
    assert "Incirlik" not in intercept_blob
    assert "french_coast" not in intercept_blob
    intercept_tool = get_mission_spec_schema("intercept", theatre="Nevada")
    assert intercept_tool["ok"] is True
    assert intercept_tool["example"]["player"]["airfield"] == "Nellis"
    assert intercept_tool["example"]["enemies"][0]["country"] == "Russia"
    cap = build_spec_schema("cap", theatre="Nevada")
    assert cap.example["theatre"] == "Nevada"
    assert cap.example["player"]["airfield"] == "Nellis"
    assert cap.example["player"]["aircraft"] == "Su-25T"
    assert cap.example["player"]["country"] == "USA"
    assert cap.example["cap"]["bearing_deg"] == 350
    assert cap.example["cap"]["distance_km"] == 40
    assert cap.example["cap"]["altitude_m"] == 4000
    assert cap.example["cap"]["bearing_deg"] != 180
    assert cap.example["cap"]["bearing_deg"] != 270
    assert cap.example["cap"]["distance_km"] != 63
    assert cap.example["enemies"][0]["country"] == "Russia"
    assert cap.example["player"]["airfield"] != "Manston"
    assert cap.example["player"]["airfield"] != "Incirlik"
    assert cap.example["player"]["airfield"] != "Batumi"
    cap_blob = " ".join(cap.notes)
    assert "nellis_north_range_cap.yaml" in cap_blob
    assert "nellis_cold_freeflight.yaml" not in cap_blob
    assert "manston_" not in cap_blob.lower()
    assert "NeedsOarPoint" not in cap_blob
    assert "french_coast" not in cap_blob
    cap_tool = get_mission_spec_schema("cap", theatre="Nevada")
    assert cap_tool["ok"] is True
    assert cap_tool["example"]["player"]["airfield"] == "Nellis"
    assert cap_tool["example"]["cap"]["bearing_deg"] == 350
    recon_tool_again = get_mission_spec_schema("recon", theatre="Nevada")
    assert recon_tool_again["ok"] is True
    blob = json.dumps({k: v for k, v in recon_tool_again["example"].items() if k != "description"})
    assert "Manston" not in blob
    assert "NeedsOarPoint" not in blob
    assert "Batumi" not in blob
    assert "Incirlik" not in blob
    assert "Hawkinge" not in blob
    assert recon_tool_again["example"]["recon"]["bearing_deg"] != 350
    assert recon_tool_again["example"]["recon"]["distance_km"] != 40


def test_schema_theatre_falklands_combat_no_manston_skeleton() -> None:
    with pytest.raises(ValueError, match="not supported for theatre Falklands"):
        build_spec_schema("recon", theatre="Falklands")
    ga = build_spec_schema("ground_attack", theatre="Falklands")
    assert ga.example["theatre"] == "Falklands"
    assert ga.example["player"]["airfield"] == "MountPleasant"
    assert ga.example["player"]["aircraft"] == "Su-25T"
    assert ga.example["player"]["country"] == "UK"
    assert ga.example["player"]["payload"] == "su25t_2x_fab250"
    assert ga.example["strike"]["bearing_deg"] == 269
    assert ga.example["strike"]["distance_km"] == 21
    assert ga.example["strike"]["altitude_m"] == 2000
    assert ga.example["strike"]["bearing_deg"] != 150
    assert ga.example["strike"]["distance_km"] != 40
    assert ga.example["targets"][0]["unit"] == "Ural-375"
    assert ga.example["targets"][0]["country"] == "Argentina"
    assert ga.example["player"]["airfield"] != "Manston"
    assert ga.example["player"]["airfield"] != "Nellis"
    assert ga.example["player"]["airfield"] != "Incirlik"
    assert ga.example["player"]["airfield"] != "Batumi"
    ga_blob = " ".join(ga.notes)
    assert "east_falkland_inland_strike" in ga_blob or "Goose Green" in ga_blob
    assert "mount_pleasant_east_falkland_ground_attack.yaml" in ga_blob
    assert "french_coast" not in ga_blob
    assert "manston_" not in ga_blob.lower()
    ga_tool = get_mission_spec_schema("ground_attack", theatre="Falklands")
    assert ga_tool["ok"] is True
    assert ga_tool["example"]["player"]["airfield"] == "MountPleasant"
    assert ga_tool["example"]["strike"]["bearing_deg"] == 269
    assert ga_tool["example"]["targets"][0]["country"] == "Argentina"
    cap = build_spec_schema("cap", theatre="Falklands")
    assert cap.example["theatre"] == "Falklands"
    assert cap.example["player"]["airfield"] == "MountPleasant"
    assert cap.example["player"]["aircraft"] == "Su-25T"
    assert cap.example["player"]["country"] == "UK"
    assert cap.example["cap"]["bearing_deg"] == 150
    assert cap.example["cap"]["distance_km"] == 40
    assert cap.example["cap"]["altitude_m"] == 4000
    assert cap.example["cap"]["bearing_deg"] != 350
    assert cap.example["cap"]["bearing_deg"] != 180
    assert cap.example["cap"]["bearing_deg"] != 270
    assert cap.example["cap"]["distance_km"] != 25
    assert cap.example["cap"]["distance_km"] != 63
    assert cap.example["enemies"][0]["country"] == "Argentina"
    cap_blob = " ".join(cap.notes)
    assert "mount_pleasant_south_atlantic_cap.yaml" in cap_blob
    assert "manston_" not in cap_blob.lower()
    assert "examples are Channel templates" not in cap_blob
    tool = get_mission_spec_schema("cap", theatre="Falklands")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "MountPleasant"
    assert tool["example"]["cap"]["bearing_deg"] == 150
    intercept = build_spec_schema("intercept", theatre="Falklands")
    assert intercept.example["theatre"] == "Falklands"
    assert intercept.example["player"]["airfield"] == "MountPleasant"
    assert intercept.example["player"]["aircraft"] == "Su-25T"
    assert intercept.example["player"]["country"] == "UK"
    assert intercept.example["enemies"][0]["country"] == "Argentina"
    intercept_blob = " ".join(intercept.notes)
    assert "mount_pleasant_dawn_intercept.yaml" in intercept_blob
    assert "manston_" not in intercept_blob.lower()
    assert "NeedsOarPoint" not in intercept_blob
    assert "Batumi" not in intercept_blob
    intercept_tool = get_mission_spec_schema("intercept", theatre="Falklands")
    assert intercept_tool["ok"] is True
    assert intercept_tool["example"]["player"]["airfield"] == "MountPleasant"
    blob = json.dumps({k: v for k, v in intercept_tool["example"].items() if k != "description"})
    assert "Manston" not in blob
    assert "NeedsOarPoint" not in blob
    assert "Batumi" not in blob
    assert "Incirlik" not in blob
    assert "Nellis" not in blob
    escort = build_spec_schema("escort", theatre="Falklands")
    assert escort.example["theatre"] == "Falklands"
    assert escort.example["player"]["airfield"] == "MountPleasant"
    assert escort.example["player"]["aircraft"] == "Su-25T"
    assert escort.example["player"]["country"] == "UK"
    assert escort.example["package"][0]["aircraft"] == "Su-25T"
    assert escort.example["package"][0]["country"] == "UK"
    assert escort.example["enemies"][0]["country"] == "Argentina"
    assert escort.example["escort"]["bearing_deg"] == 150
    assert escort.example["escort"]["distance_km"] == 40
    assert escort.example["escort"]["altitude_m"] == 4000
    assert escort.example["escort"]["bearing_deg"] != 120
    assert escort.example["escort"]["bearing_deg"] != 350
    assert escort.example["escort"]["distance_km"] != 55
    assert escort.example["player"]["airfield"] != "Manston"
    assert escort.example["player"]["airfield"] != "Nellis"
    escort_blob = " ".join(escort.notes)
    assert "mount_pleasant_south_atlantic_escort.yaml" in escort_blob
    assert "manston_" not in escort_blob.lower()
    assert "NeedsOarPoint" not in escort_blob
    assert "french_coast" not in escort_blob
    escort_tool = get_mission_spec_schema("escort", theatre="Falklands")
    assert escort_tool["ok"] is True
    assert escort_tool["example"]["player"]["airfield"] == "MountPleasant"
    assert escort_tool["example"]["package"][0]["country"] == "UK"
    assert escort_tool["example"]["enemies"][0]["country"] == "Argentina"
    assert escort_tool["example"]["escort"]["bearing_deg"] == 150
    recon = get_mission_spec_schema("recon", theatre="Falklands")
    assert recon["ok"] is False
    assert recon["code"] == "combat_unsupported_theatre"


def test_schema_theatre_caucasus_combat_no_manston_skeleton() -> None:
    ga = build_spec_schema("ground_attack", theatre="Caucasus")
    assert ga.example["theatre"] == "Caucasus"
    assert ga.example["player"]["airfield"] == "Batumi"
    assert ga.example["player"]["aircraft"] == "Su-25T"
    assert ga.example["player"]["payload"] == "su25t_2x_fab250"
    assert ga.example["strike"]["bearing_deg"] == 43
    assert ga.example["strike"]["distance_km"] == 110
    assert ga.example["targets"][0]["unit"] == "Ural-375"
    assert ga.example["targets"][0]["country"] == "Russia"
    ga_blob = " ".join(ga.notes)
    assert "kutaisi_inland_strike" in ga_blob or "Kutaisi" in ga_blob
    assert "french_coast" not in ga_blob
    assert "manston_" not in ga_blob.lower()
    cap = build_spec_schema("cap", theatre="Caucasus")
    assert cap.example["theatre"] == "Caucasus"
    assert cap.example["player"]["airfield"] == "Batumi"
    assert cap.example["player"]["aircraft"] == "Su-25T"
    assert cap.example["cap"]["bearing_deg"] == 270
    assert cap.example["cap"]["distance_km"] == 40
    assert cap.example["enemies"][0]["country"] == "Russia"
    tool = get_mission_spec_schema("cap", theatre="Caucasus")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "Batumi"
    intercept = get_mission_spec_schema("intercept", theatre="Caucasus")
    assert intercept["ok"] is True
    assert intercept["example"]["player"]["airfield"] == "Batumi"
    assert intercept["example"]["player"]["aircraft"] == "Su-25T"
    assert intercept["example"]["enemies"][0]["country"] == "Russia"
    intercept_blob = json.dumps(intercept)
    assert "Manston" not in intercept_blob
    assert "NeedsOarPoint" not in intercept_blob
    escort = get_mission_spec_schema("escort", theatre="Caucasus")
    assert escort["ok"] is True
    assert escort["example"]["theatre"] == "Caucasus"
    assert escort["example"]["player"]["airfield"] == "Batumi"
    assert escort["example"]["player"]["aircraft"] == "Su-25T"
    assert escort["example"]["package"][0]["aircraft"] == "Su-25T"
    assert escort["example"]["package"][0]["country"] == "Georgia"
    assert escort["example"]["enemies"][0]["country"] == "Russia"
    assert escort["example"]["escort"]["bearing_deg"] == 270
    assert escort["example"]["escort"]["distance_km"] == 40
    escort_blob = json.dumps(escort)
    assert "Manston" not in escort_blob
    assert "NeedsOarPoint" not in escort_blob
    assert "120" not in str(escort["example"]["escort"]["bearing_deg"])
    assert "MosquitoFBMkVI" not in escort_blob
    assert "Bf-109K-4" not in escort_blob
    recon = get_mission_spec_schema("recon", theatre="Caucasus")
    assert recon["ok"] is True
    assert recon["example"]["theatre"] == "Caucasus"
    assert recon["example"]["player"]["airfield"] == "Batumi"
    assert recon["example"]["player"]["aircraft"] == "Su-25T"
    assert recon["example"]["recon"]["bearing_deg"] == 43
    assert recon["example"]["recon"]["distance_km"] == 110
    assert recon["example"]["targets"][0]["unit"] == "Ural-375"
    assert recon["example"]["targets"][0]["country"] == "Russia"
    assert recon["example"]["player"]["airfield"] != "Manston"
    assert recon["example"]["player"]["airfield"] != "NeedsOarPoint"
    recon_notes = " ".join(build_spec_schema("recon", theatre="Caucasus").notes)
    assert "kutaisi_inland_strike" in recon_notes or "Kutaisi" in recon_notes
    assert "french_coast" not in recon_notes
    assert "manston_" not in recon_notes.lower()


def test_era_filter_channel_rejects_georgia_turkey_and_su25t() -> None:
    spec = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"country": "Georgia"})
        }
    )
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "unknown_country" for e in result.errors)
    spec_tr = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"country": "Turkey"})
        }
    )
    result_tr = validate_mission_spec(spec_tr, inventory=_inv())
    assert not result_tr.ok
    assert any(e.code == "unknown_country" for e in result_tr.errors)
    spec_usa = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"country": "USA"})
        }
    )
    result_usa = validate_mission_spec(spec_usa, inventory=_inv())
    assert not result_usa.ok
    assert any(e.code == "unknown_country" for e in result_usa.errors)
    spec_ru = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"country": "Russia"})
        }
    )
    result_ru = validate_mission_spec(spec_ru, inventory=_inv())
    assert not result_ru.ok
    assert any(e.code == "unknown_country" for e in result_ru.errors)
    spec_sy = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"country": "Syria"})
        }
    )
    result_sy = validate_mission_spec(spec_sy, inventory=_inv())
    assert not result_sy.ok
    assert any(e.code == "unknown_country" for e in result_sy.errors)
    spec_ar = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(
                update={"country": "Argentina"}
            )
        }
    )
    result_ar = validate_mission_spec(spec_ar, inventory=_inv())
    assert not result_ar.ok
    assert any(e.code == "unknown_country" for e in result_ar.errors)
    spec_ac = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"aircraft": "Su-25T"})
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert not result_ac.ok
    assert any(e.code == "unknown_aircraft" for e in result_ac.errors)


def test_era_filter_caucasus_accepts_spitfire() -> None:
    spec_uk = load_mission_spec(CAUCASUS_FF).model_copy(
        update={
            "player": load_mission_spec(CAUCASUS_FF).player.model_copy(update={"country": "UK"})
        }
    )
    result_uk = validate_mission_spec(spec_uk, inventory=_inv())
    assert result_uk.ok, result_uk.errors
    spec_ac = load_mission_spec(CAUCASUS_FF).model_copy(
        update={
            "player": load_mission_spec(CAUCASUS_FF).player.model_copy(
                update={"aircraft": "SpitfireLFMkIX"}
            )
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert result_ac.ok, result_ac.errors


def test_era_filter_syria_accepts_spitfire() -> None:
    spec_uk = load_mission_spec(SYRIA_FF).model_copy(
        update={"player": load_mission_spec(SYRIA_FF).player.model_copy(update={"country": "UK"})}
    )
    result_uk = validate_mission_spec(spec_uk, inventory=_inv())
    assert result_uk.ok, result_uk.errors
    spec_ac = load_mission_spec(SYRIA_FF).model_copy(
        update={
            "player": load_mission_spec(SYRIA_FF).player.model_copy(
                update={"aircraft": "SpitfireLFMkIX"}
            )
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert result_ac.ok, result_ac.errors


def test_era_filter_nevada_accepts_spitfire() -> None:
    spec_uk = load_mission_spec(NEVADA_FF).model_copy(
        update={"player": load_mission_spec(NEVADA_FF).player.model_copy(update={"country": "UK"})}
    )
    result_uk = validate_mission_spec(spec_uk, inventory=_inv())
    assert result_uk.ok, result_uk.errors
    spec_ac = load_mission_spec(NEVADA_FF).model_copy(
        update={
            "player": load_mission_spec(NEVADA_FF).player.model_copy(
                update={"aircraft": "SpitfireLFMkIX"}
            )
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert result_ac.ok, result_ac.errors


def test_era_filter_falklands_accepts_spitfire() -> None:
    spec = load_mission_spec(FALKLANDS_FF)
    assert validate_mission_spec(spec, inventory=_inv()).ok
    spec_ac = load_mission_spec(FALKLANDS_FF).model_copy(
        update={
            "player": load_mission_spec(FALKLANDS_FF).player.model_copy(
                update={"aircraft": "SpitfireLFMkIX"}
            )
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert result_ac.ok, result_ac.errors


def test_era_filter_caucasus_georgia_and_syria_turkey_ok() -> None:
    caucasus = load_mission_spec(CAUCASUS_FF)
    assert validate_mission_spec(caucasus, inventory=_inv()).ok
    syria = load_mission_spec(SYRIA_FF)
    assert validate_mission_spec(syria, inventory=_inv()).ok
    nevada = load_mission_spec(NEVADA_FF)
    assert validate_mission_spec(nevada, inventory=_inv()).ok
    falklands = load_mission_spec(FALKLANDS_FF)
    assert validate_mission_spec(falklands, inventory=_inv()).ok


def test_caucasus_cap_invent_nudge() -> None:
    spec = load_mission_spec(CAUCASUS_CAP)
    assert host_normandy_combat_nudge(spec) is None
    intercept = load_mission_spec(CAUCASUS_INTERCEPT)
    assert host_normandy_combat_nudge(intercept) is None
    escort = load_mission_spec(CAUCASUS_ESCORT)
    assert host_normandy_combat_nudge(escort) is None
    recon = load_mission_spec(CAUCASUS_RECON)
    assert host_normandy_combat_nudge(recon) is None
    ff = load_mission_spec(CAUCASUS_FF)
    assert host_normandy_combat_nudge(ff) is None


def test_syria_cap_invent_nudge() -> None:
    spec = load_mission_spec(SYRIA_CAP)
    assert host_normandy_combat_nudge(spec) is None
    intercept = load_mission_spec(SYRIA_INTERCEPT)
    assert host_normandy_combat_nudge(intercept) is None
    escort = load_mission_spec(SYRIA_ESCORT)
    assert host_normandy_combat_nudge(escort) is None
    ga = load_mission_spec(SYRIA_GA)
    assert host_normandy_combat_nudge(ga) is None
    recon = load_mission_spec(SYRIA_RECON)
    assert host_normandy_combat_nudge(recon) is None
    ff = load_mission_spec(SYRIA_FF)
    assert host_normandy_combat_nudge(ff) is None


def test_nevada_cap_invent_nudge() -> None:
    spec = load_mission_spec(NEVADA_CAP)
    assert host_normandy_combat_nudge(spec) is None
    intercept = load_mission_spec(NEVADA_INTERCEPT)
    assert host_normandy_combat_nudge(intercept) is None
    escort = load_mission_spec(NEVADA_ESCORT)
    assert host_normandy_combat_nudge(escort) is None
    ga = load_mission_spec(NEVADA_GA)
    assert host_normandy_combat_nudge(ga) is None
    recon = load_mission_spec(NEVADA_RECON)
    assert host_normandy_combat_nudge(recon) is None
    ff = load_mission_spec(NEVADA_FF)
    assert host_normandy_combat_nudge(ff) is None


def test_falklands_cap_invent_nudge() -> None:
    spec = load_mission_spec(FALKLANDS_CAP)
    assert host_normandy_combat_nudge(spec) is None
    ff = load_mission_spec(FALKLANDS_FF)
    assert host_normandy_combat_nudge(ff) is None
    intercept = load_mission_spec(FALKLANDS_INTERCEPT)
    assert host_normandy_combat_nudge(intercept) is None
    escort = load_mission_spec(FALKLANDS_ESCORT)
    assert host_normandy_combat_nudge(escort) is None
    ga = load_mission_spec(FALKLANDS_GA)
    assert host_normandy_combat_nudge(ga) is None
    recon = load_mission_spec(NEVADA_RECON).model_copy(
        update={"theatre": "Falklands", "player": load_mission_spec(FALKLANDS_FF).player}
    )
    assert host_normandy_combat_nudge(recon) is not None


def test_schema_theatre_normandy_free_flight() -> None:
    view = build_spec_schema("free_flight", theatre="Normandy")
    assert view.example["theatre"] == "Normandy"
    assert view.example["player"]["airfield"] == "NeedsOarPoint"
    assert view.example["player"]["airfield"] != "Manston"
    tool = get_mission_spec_schema("free_flight", theatre="Normandy")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "NeedsOarPoint"


def test_schema_theatre_normandy_combat_no_manston_skeleton() -> None:
    recon = build_spec_schema("recon", theatre="Normandy")
    assert recon.example["theatre"] == "Normandy"
    assert recon.example["player"]["airfield"] == "NeedsOarPoint"
    assert recon.example["player"]["airfield"] != "Manston"
    assert recon.example["recon"]["bearing_deg"] == 180
    assert recon.example["recon"]["distance_km"] == 133
    assert recon.example["recon"]["bearing_deg"] != 125
    assert recon.example["recon"]["distance_km"] != 76
    recon_notes = " ".join(recon.notes)
    assert "french_coast" not in recon_notes
    assert "Maupertus" in recon_notes or "133" in recon_notes
    escort = build_spec_schema("escort", theatre="Normandy")
    assert escort.example["theatre"] == "Normandy"
    assert escort.example["player"]["airfield"] == "NeedsOarPoint"
    assert escort.example["player"]["airfield"] != "Manston"
    assert escort.example["escort"]["bearing_deg"] == 180
    assert escort.example["escort"]["distance_km"] == 63
    assert escort.example["escort"]["bearing_deg"] != 120
    assert escort.example["escort"]["distance_km"] != 55
    escort_notes = " ".join(escort.notes)
    assert "french_coast" not in escort_notes
    assert "120/55" not in escort_notes or "not Manston 120/55" in escort_notes
    ix = build_spec_schema("intercept", theatre="Normandy")
    assert ix.example["theatre"] == "Normandy"
    assert ix.example["player"]["airfield"] == "NeedsOarPoint"
    assert ix.example["player"]["airfield"] != "Manston"
    assert ix.example["mission_type"] == "intercept"
    ix_notes = " ".join(ix.notes)
    assert "french_coast" not in ix_notes
    assert "manston_dawn_intercept_radio" not in ix_notes
    assert "Cherbourg" in ix_notes or "63" in ix_notes
    ga = build_spec_schema("ground_attack", theatre="Normandy")
    assert ga.example["theatre"] == "Normandy"
    assert ga.example["player"]["airfield"] == "NeedsOarPoint"
    assert ga.example["player"]["airfield"] != "Manston"
    assert ga.example["strike"]["bearing_deg"] == 180
    assert ga.example["strike"]["distance_km"] == 133
    assert ga.example["strike"]["bearing_deg"] != 125
    assert ga.example["strike"]["distance_km"] != 76
    notes = " ".join(ga.notes)
    assert "french_coast" not in notes
    assert "Maupertus" in notes or "133" in notes
    cap = build_spec_schema("cap", theatre="Normandy")
    assert cap.example["theatre"] == "Normandy"
    assert cap.example["player"]["airfield"] == "NeedsOarPoint"
    assert cap.example["player"]["airfield"] != "Manston"
    assert cap.example["cap"]["bearing_deg"] == 180
    assert cap.example["cap"]["distance_km"] == 63
    assert cap.example["cap"]["bearing_deg"] != 135
    assert cap.example["cap"]["distance_km"] != 25


def test_stub_default_stays_manston() -> None:
    from dcs_miz_planner.agent.llm import (
        BATUMI_COLD_FREE_FLIGHT_JSON,
        INCIRLIK_COLD_FREE_FLIGHT_JSON,
        MOUNT_PLEASANT_COLD_FREE_FLIGHT_JSON,
        NELLIS_COLD_FREE_FLIGHT_JSON,
    )

    stub = json.loads(MANSTON_FREE_FLIGHT_JSON)
    assert stub["theatre"] == "TheChannel"
    assert stub["player"]["airfield"] == "Manston"
    test_only = json.loads(NEEDS_OAR_POINT_FREE_FLIGHT_JSON)
    assert test_only["player"]["airfield"] == "NeedsOarPoint"
    batumi = json.loads(BATUMI_COLD_FREE_FLIGHT_JSON)
    assert batumi["player"]["airfield"] == "Batumi"
    assert batumi["theatre"] == "Caucasus"
    incirlik = json.loads(INCIRLIK_COLD_FREE_FLIGHT_JSON)
    assert incirlik["player"]["airfield"] == "Incirlik"
    assert incirlik["theatre"] == "Syria"
    assert incirlik["player"]["country"] == "Turkey"
    nellis = json.loads(NELLIS_COLD_FREE_FLIGHT_JSON)
    assert nellis["player"]["airfield"] == "Nellis"
    assert nellis["theatre"] == "Nevada"
    assert nellis["player"]["country"] == "USA"
    mount = json.loads(MOUNT_PLEASANT_COLD_FREE_FLIGHT_JSON)
    assert mount["player"]["airfield"] == "MountPleasant"
    assert mount["theatre"] == "Falklands"
    assert mount["player"]["country"] == "UK"


def test_normandy_combat_invent_nudge() -> None:
    ff = load_mission_spec(NORMANDY_FF)
    assert host_normandy_combat_nudge(ff) is None
    assert host_normandy_combat_nudge(load_mission_spec(NORMANDY_CAP)) is None
    assert host_normandy_combat_nudge(load_mission_spec(NORMANDY_GA)) is None
    assert host_normandy_combat_nudge(load_mission_spec(NORMANDY_INTERCEPT)) is None
    assert host_normandy_combat_nudge(load_mission_spec(NORMANDY_ESCORT)) is None
    assert host_normandy_combat_nudge(load_mission_spec(NORMANDY_RECON)) is None


def test_chat_normandy_recon_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    recon_json = load_mission_spec(NORMANDY_RECON).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Normandy recon inland of Maupertus")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "recon"
    assert session.proposed_spec.player.airfield == "NeedsOarPoint"
    assert session.proposed_spec.theatre == "Normandy"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "recon"
    assert written.player.airfield == "NeedsOarPoint"


def test_planner_normandy_recon_is_written(tmp_path: Path) -> None:
    recon_json = load_mission_spec(NORMANDY_RECON).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Normandy recon inland of Maupertus",
        out,
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None


def test_chat_caucasus_cap_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = load_mission_spec(CAUCASUS_CAP).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Caucasus CAP west of Batumi")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "cap"
    assert session.proposed_spec.player.airfield == "Batumi"
    assert session.proposed_spec.theatre == "Caucasus"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "cap"
    assert written.player.airfield == "Batumi"


def test_planner_caucasus_cap_is_written(tmp_path: Path) -> None:
    cap_json = load_mission_spec(CAUCASUS_CAP).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Caucasus CAP west of Batumi",
        out,
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Caucasus"
    assert result.spec.mission_type.value == "cap"
    assert result.spec.player.airfield == "Batumi"
    assert result.spec.cap is not None
    assert result.spec.cap.bearing_deg == 270
    assert result.spec.cap.distance_km == 40


def test_planner_caucasus_ground_attack_is_written(tmp_path: Path) -> None:
    ga_json = load_mission_spec(CAUCASUS_GA).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Caucasus ground attack inland of Kutaisi",
        out,
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Caucasus"
    assert result.spec.mission_type.value == "ground_attack"
    assert result.spec.player.airfield == "Batumi"
    assert result.spec.strike is not None
    assert result.spec.strike.bearing_deg == 43
    assert result.spec.strike.distance_km == 110


def test_chat_caucasus_intercept_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    intercept_json = load_mission_spec(CAUCASUS_INTERCEPT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Caucasus intercept")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "intercept"
    assert session.proposed_spec.player.airfield == "Batumi"
    assert session.proposed_spec.theatre == "Caucasus"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "intercept"
    assert written.player.airfield == "Batumi"


def test_planner_caucasus_intercept_is_written(tmp_path: Path) -> None:
    intercept_json = load_mission_spec(CAUCASUS_INTERCEPT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Caucasus intercept west of Batumi",
        out,
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Caucasus"
    assert result.spec.mission_type.value == "intercept"
    assert result.spec.player.airfield == "Batumi"


def test_chat_caucasus_escort_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    escort_json = load_mission_spec(CAUCASUS_ESCORT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Caucasus escort")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "escort"
    assert session.proposed_spec.player.airfield == "Batumi"
    assert session.proposed_spec.theatre == "Caucasus"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "escort"
    assert written.player.airfield == "Batumi"
    assert written.escort is not None
    assert written.escort.bearing_deg == 270
    assert written.escort.distance_km == 40
    assert written.package[0].aircraft == "Su-25T"
    assert written.package[0].country == "Georgia"


def test_planner_caucasus_escort_is_written(tmp_path: Path) -> None:
    escort_json = load_mission_spec(CAUCASUS_ESCORT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Caucasus escort west of Batumi",
        out,
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Caucasus"
    assert result.spec.mission_type.value == "escort"
    assert result.spec.player.airfield == "Batumi"
    assert result.spec.escort is not None
    assert result.spec.escort.bearing_deg == 270
    assert result.spec.escort.distance_km == 40


def test_chat_caucasus_recon_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    recon_json = load_mission_spec(CAUCASUS_RECON).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Caucasus recon inland of Kutaisi")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "recon"
    assert session.proposed_spec.player.airfield == "Batumi"
    assert session.proposed_spec.theatre == "Caucasus"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "recon"
    assert written.player.airfield == "Batumi"
    assert written.recon is not None
    assert written.recon.bearing_deg == 43
    assert written.recon.distance_km == 110
    assert written.targets[0].unit == "Ural-375"
    assert written.targets[0].country == "Russia"


def test_planner_caucasus_recon_is_written(tmp_path: Path) -> None:
    recon_json = load_mission_spec(CAUCASUS_RECON).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Caucasus recon inland of Kutaisi",
        out,
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Caucasus"
    assert result.spec.mission_type.value == "recon"
    assert result.spec.player.airfield == "Batumi"
    assert result.spec.recon is not None
    assert result.spec.recon.bearing_deg == 43
    assert result.spec.recon.distance_km == 110


def test_chat_syria_cap_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = load_mission_spec(SYRIA_CAP).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Syria CAP south of Incirlik")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "cap"
    assert session.proposed_spec.player.airfield == "Incirlik"
    assert session.proposed_spec.theatre == "Syria"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "cap"
    assert written.player.airfield == "Incirlik"
    assert written.cap is not None
    assert written.cap.bearing_deg == 180
    assert written.cap.distance_km == 40


def test_planner_syria_cap_is_written(tmp_path: Path) -> None:
    cap_json = load_mission_spec(SYRIA_CAP).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Syria CAP south of Incirlik",
        out,
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Syria"
    assert result.spec.mission_type.value == "cap"
    assert result.spec.player.airfield == "Incirlik"
    assert result.spec.cap is not None
    assert result.spec.cap.bearing_deg == 180
    assert result.spec.cap.distance_km == 40


def test_chat_syria_intercept_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    intercept_json = load_mission_spec(SYRIA_INTERCEPT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Syria intercept south of Incirlik")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "intercept"
    assert session.proposed_spec.player.airfield == "Incirlik"
    assert session.proposed_spec.theatre == "Syria"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "intercept"
    assert written.player.airfield == "Incirlik"


def test_planner_syria_intercept_is_written(tmp_path: Path) -> None:
    intercept_json = load_mission_spec(SYRIA_INTERCEPT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Syria intercept south of Incirlik",
        out,
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Syria"
    assert result.spec.mission_type.value == "intercept"
    assert result.spec.player.airfield == "Incirlik"


def test_chat_syria_escort_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    escort_json = load_mission_spec(SYRIA_ESCORT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Syria escort south of Incirlik")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "escort"
    assert session.proposed_spec.player.airfield == "Incirlik"
    assert session.proposed_spec.theatre == "Syria"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "escort"
    assert written.player.airfield == "Incirlik"
    assert written.escort is not None
    assert written.escort.bearing_deg == 180
    assert written.escort.distance_km == 40
    assert written.package[0].aircraft == "Su-25T"
    assert written.package[0].country == "Turkey"


def test_planner_syria_escort_is_written(tmp_path: Path) -> None:
    escort_json = load_mission_spec(SYRIA_ESCORT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Syria escort south of Incirlik",
        out,
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Syria"
    assert result.spec.mission_type.value == "escort"
    assert result.spec.player.airfield == "Incirlik"
    assert result.spec.escort is not None
    assert result.spec.escort.bearing_deg == 180
    assert result.spec.escort.distance_km == 40


def test_chat_syria_ga_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    ga_json = load_mission_spec(SYRIA_GA).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Syria ground attack inland past Aleppo")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "ground_attack"
    assert session.proposed_spec.player.airfield == "Incirlik"
    assert session.proposed_spec.theatre == "Syria"
    assert session.proposed_spec.strike is not None
    assert session.proposed_spec.strike.bearing_deg == 121
    assert session.proposed_spec.strike.distance_km == 200
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "ground_attack"
    assert written.player.airfield == "Incirlik"
    assert written.targets[0].unit == "Ural-375"
    assert written.targets[0].country == "Syria"


def test_planner_syria_ground_attack_is_written(tmp_path: Path) -> None:
    ga_json = load_mission_spec(SYRIA_GA).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Syria ground attack inland past Aleppo",
        out,
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Syria"
    assert result.spec.mission_type.value == "ground_attack"
    assert result.spec.player.airfield == "Incirlik"
    assert result.spec.strike is not None
    assert result.spec.strike.bearing_deg == 121
    assert result.spec.strike.distance_km == 200
    assert result.spec.targets[0].unit == "Ural-375"
    assert result.spec.targets[0].country == "Syria"


def test_chat_syria_recon_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    recon_json = load_mission_spec(SYRIA_RECON).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Syria recon inland past Aleppo")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "recon"
    assert session.proposed_spec.player.airfield == "Incirlik"
    assert session.proposed_spec.theatre == "Syria"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "recon"
    assert written.player.airfield == "Incirlik"
    assert written.recon is not None
    assert written.recon.bearing_deg == 121
    assert written.recon.distance_km == 200
    assert written.targets[0].unit == "Ural-375"
    assert written.targets[0].country == "Syria"


def test_planner_syria_recon_is_written(tmp_path: Path) -> None:
    recon_json = load_mission_spec(SYRIA_RECON).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Syria recon inland past Aleppo",
        out,
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Syria"
    assert result.spec.mission_type.value == "recon"
    assert result.spec.player.airfield == "Incirlik"
    assert result.spec.recon is not None
    assert result.spec.recon.bearing_deg == 121
    assert result.spec.recon.distance_km == 200
    assert result.spec.targets[0].unit == "Ural-375"
    assert result.spec.targets[0].country == "Syria"


def test_chat_nevada_cap_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = load_mission_spec(NEVADA_CAP).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Nevada CAP north of Nellis")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "cap"
    assert session.proposed_spec.player.airfield == "Nellis"
    assert session.proposed_spec.theatre == "Nevada"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "cap"
    assert written.player.airfield == "Nellis"
    assert written.cap is not None
    assert written.cap.bearing_deg == 350
    assert written.cap.distance_km == 40


def test_planner_nevada_cap_is_written(tmp_path: Path) -> None:
    cap_json = load_mission_spec(NEVADA_CAP).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Nevada CAP north of Nellis",
        out,
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Nevada"
    assert result.spec.mission_type.value == "cap"
    assert result.spec.player.airfield == "Nellis"
    assert result.spec.cap is not None
    assert result.spec.cap.bearing_deg == 350
    assert result.spec.cap.distance_km == 40
    assert result.spec.enemies[0].country == "Russia"


def test_chat_nevada_intercept_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    intercept_json = load_mission_spec(NEVADA_INTERCEPT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Nevada intercept north of Nellis")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "intercept"
    assert session.proposed_spec.player.airfield == "Nellis"
    assert session.proposed_spec.theatre == "Nevada"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "intercept"
    assert written.player.airfield == "Nellis"
    assert written.enemies[0].country == "Russia"


def test_planner_nevada_intercept_is_written(tmp_path: Path) -> None:
    intercept_json = load_mission_spec(NEVADA_INTERCEPT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Nevada intercept north of Nellis",
        out,
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Nevada"
    assert result.spec.mission_type.value == "intercept"
    assert result.spec.player.airfield == "Nellis"
    assert result.spec.enemies[0].country == "Russia"


def test_chat_nevada_escort_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    escort_json = load_mission_spec(NEVADA_ESCORT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Nevada escort north of Nellis")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "escort"
    assert session.proposed_spec.player.airfield == "Nellis"
    assert session.proposed_spec.theatre == "Nevada"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "escort"
    assert written.player.airfield == "Nellis"
    assert written.escort is not None
    assert written.escort.bearing_deg == 350
    assert written.escort.distance_km == 40
    assert written.package[0].aircraft == "Su-25T"
    assert written.package[0].country == "USA"
    assert written.enemies[0].country == "Russia"


def test_planner_nevada_escort_is_written(tmp_path: Path) -> None:
    escort_json = load_mission_spec(NEVADA_ESCORT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Nevada escort north of Nellis",
        out,
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Nevada"
    assert result.spec.mission_type.value == "escort"
    assert result.spec.player.airfield == "Nellis"
    assert result.spec.escort is not None
    assert result.spec.escort.bearing_deg == 350
    assert result.spec.escort.distance_km == 40
    assert result.spec.package[0].country == "USA"
    assert result.spec.enemies[0].country == "Russia"


def test_chat_nevada_ga_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    ga_json = load_mission_spec(NEVADA_GA).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Nevada ground attack inland past Creech")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "ground_attack"
    assert session.proposed_spec.player.airfield == "Nellis"
    assert session.proposed_spec.theatre == "Nevada"
    assert session.proposed_spec.strike is not None
    assert session.proposed_spec.strike.bearing_deg == 303
    assert session.proposed_spec.strike.distance_km == 85
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "ground_attack"
    assert written.player.airfield == "Nellis"
    assert written.targets[0].unit == "Ural-375"
    assert written.targets[0].country == "Russia"


def test_planner_nevada_ground_attack_is_written(tmp_path: Path) -> None:
    ga_json = load_mission_spec(NEVADA_GA).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Nevada ground attack inland past Creech",
        out,
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Nevada"
    assert result.spec.mission_type.value == "ground_attack"
    assert result.spec.player.airfield == "Nellis"
    assert result.spec.strike is not None
    assert result.spec.strike.bearing_deg == 303
    assert result.spec.strike.distance_km == 85
    assert result.spec.targets[0].unit == "Ural-375"
    assert result.spec.targets[0].country == "Russia"


def test_chat_nevada_recon_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    recon_json = load_mission_spec(NEVADA_RECON).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Nevada recon inland past Creech")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "recon"
    assert session.proposed_spec.player.airfield == "Nellis"
    assert session.proposed_spec.theatre == "Nevada"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "recon"
    assert written.player.airfield == "Nellis"
    assert written.recon is not None
    assert written.recon.bearing_deg == 303
    assert written.recon.distance_km == 85
    assert written.targets[0].unit == "Ural-375"
    assert written.targets[0].country == "Russia"


def test_planner_nevada_recon_is_written(tmp_path: Path) -> None:
    recon_json = load_mission_spec(NEVADA_RECON).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Nevada recon inland past Creech",
        out,
        llm=StubLLM(script=[LLMResponse(content=recon_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Nevada"
    assert result.spec.mission_type.value == "recon"
    assert result.spec.player.airfield == "Nellis"
    assert result.spec.recon is not None
    assert result.spec.recon.bearing_deg == 303
    assert result.spec.recon.distance_km == 85
    assert result.spec.targets[0].unit == "Ural-375"
    assert result.spec.targets[0].country == "Russia"


def test_chat_falklands_cap_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = load_mission_spec(FALKLANDS_CAP).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Falklands CAP south of Mount Pleasant")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "cap"
    assert session.proposed_spec.player.airfield == "MountPleasant"
    assert session.proposed_spec.theatre == "Falklands"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "cap"
    assert written.player.airfield == "MountPleasant"
    assert written.cap is not None
    assert written.cap.bearing_deg == 150
    assert written.cap.distance_km == 40
    assert written.enemies[0].country == "Argentina"


def test_planner_falklands_cap_is_written(tmp_path: Path) -> None:
    cap_json = load_mission_spec(FALKLANDS_CAP).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Falklands CAP south of Mount Pleasant",
        out,
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Falklands"
    assert result.spec.mission_type.value == "cap"
    assert result.spec.player.airfield == "MountPleasant"
    assert result.spec.cap is not None
    assert result.spec.cap.bearing_deg == 150
    assert result.spec.cap.distance_km == 40
    assert result.spec.enemies[0].country == "Argentina"


def test_chat_falklands_intercept_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    intercept_json = load_mission_spec(FALKLANDS_INTERCEPT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Falklands intercept south of Mount Pleasant")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "intercept"
    assert session.proposed_spec.player.airfield == "MountPleasant"
    assert session.proposed_spec.theatre == "Falklands"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "intercept"
    assert written.player.airfield == "MountPleasant"
    assert written.enemies[0].country == "Argentina"


def test_planner_falklands_intercept_is_written(tmp_path: Path) -> None:
    intercept_json = load_mission_spec(FALKLANDS_INTERCEPT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Falklands intercept south of Mount Pleasant",
        out,
        llm=StubLLM(script=[LLMResponse(content=intercept_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Falklands"
    assert result.spec.mission_type.value == "intercept"
    assert result.spec.player.airfield == "MountPleasant"
    assert result.spec.enemies[0].country == "Argentina"


def test_chat_falklands_escort_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    escort_json = load_mission_spec(FALKLANDS_ESCORT).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Falklands escort south of Mount Pleasant")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "escort"
    assert session.proposed_spec.player.airfield == "MountPleasant"
    assert session.proposed_spec.theatre == "Falklands"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "escort"
    assert written.player.airfield == "MountPleasant"
    assert written.escort is not None
    assert written.escort.bearing_deg == 150
    assert written.escort.distance_km == 40
    assert written.package[0].country == "UK"
    assert written.enemies[0].country == "Argentina"


def test_planner_falklands_escort_is_written(tmp_path: Path) -> None:
    escort_json = load_mission_spec(FALKLANDS_ESCORT).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Falklands escort south of Mount Pleasant",
        out,
        llm=StubLLM(script=[LLMResponse(content=escort_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Falklands"
    assert result.spec.mission_type.value == "escort"
    assert result.spec.player.airfield == "MountPleasant"
    assert result.spec.escort is not None
    assert result.spec.escort.bearing_deg == 150
    assert result.spec.escort.distance_km == 40
    assert result.spec.package[0].country == "UK"
    assert result.spec.enemies[0].country == "Argentina"


def test_chat_falklands_ga_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    ga_json = load_mission_spec(FALKLANDS_GA).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Falklands ground attack inland short of Goose Green")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "ground_attack"
    assert session.proposed_spec.player.airfield == "MountPleasant"
    assert session.proposed_spec.theatre == "Falklands"
    assert session.proposed_spec.strike is not None
    assert session.proposed_spec.strike.bearing_deg == 269
    assert session.proposed_spec.strike.distance_km == 21
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "ground_attack"
    assert written.player.airfield == "MountPleasant"
    assert written.targets[0].unit == "Ural-375"
    assert written.targets[0].country == "Argentina"


def test_planner_falklands_ground_attack_is_written(tmp_path: Path) -> None:
    ga_json = load_mission_spec(FALKLANDS_GA).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Falklands ground attack inland short of Goose Green",
        out,
        llm=StubLLM(script=[LLMResponse(content=ga_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Falklands"
    assert result.spec.mission_type.value == "ground_attack"
    assert result.spec.player.airfield == "MountPleasant"
    assert result.spec.strike is not None
    assert result.spec.strike.bearing_deg == 269
    assert result.spec.strike.distance_km == 21
    assert result.spec.targets[0].unit == "Ural-375"
    assert result.spec.targets[0].country == "Argentina"


def test_chat_normandy_cap_is_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = load_mission_spec(NORMANDY_CAP).model_dump_json()
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    session.handle_line("Normandy CAP toward Cherbourg")
    assert session.proposed_spec is not None
    assert session.proposed_spec.mission_type.value == "cap"
    assert session.proposed_spec.player.airfield == "NeedsOarPoint"
    assert session.proposed_spec.theatre == "Normandy"
    accepted = session.handle_line("/accept")
    assert out.exists()
    assert "Wrote Spec" in accepted.output
    written = load_mission_spec(out)
    assert written.mission_type.value == "cap"
    assert written.player.airfield == "NeedsOarPoint"


def test_planner_normandy_cap_is_written(tmp_path: Path) -> None:
    cap_json = load_mission_spec(NORMANDY_CAP).model_dump_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Normandy CAP toward Cherbourg",
        out,
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is True
    assert out.exists()
    assert result.spec is not None
    assert host_normandy_combat_nudge(result.spec) is None
    assert result.spec.theatre == "Normandy"
    assert result.spec.mission_type.value == "cap"
    assert result.spec.player.airfield == "NeedsOarPoint"
    assert result.spec.cap is not None
    assert result.spec.cap.bearing_deg == 180
    assert result.spec.cap.distance_km == 63


def test_list_mission_options_theatre_filters_channel_place(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).ensure_synced()
    channel = list_mission_options(theatre="TheChannel", db_path=db)
    assert channel["ok"] is True
    channel_ids = {o["id"] for o in channel["options"] if o["family"] == "channel_place"}
    assert "cherbourg_channel_cap" not in channel_ids
    assert "needs_oar_point_home" not in channel_ids
    assert "maupertus_inland_strike" not in channel_ids
    assert "batumi_home" not in channel_ids
    assert "batumi_black_sea_cap" not in channel_ids
    assert "incirlik_home" not in channel_ids
    assert "incirlik_iskenderun_cap" not in channel_ids
    assert "nellis_home" not in channel_ids
    assert "nellis_north_range_cap" not in channel_ids
    assert "mount_pleasant_home" not in channel_ids
    assert "mount_pleasant_south_atlantic_cap" not in channel_ids
    assert "manston_home" in channel_ids
    assert "french_coast_strike_belt" in channel_ids
    assert any(o["family"] == "weather" for o in channel["options"])
    normandy = list_mission_options(theatre="Normandy", db_path=db)
    assert normandy["ok"] is True
    normandy_ids = {o["id"] for o in normandy["options"] if o["family"] == "channel_place"}
    assert "manston_home" not in normandy_ids
    assert "french_coast_strike_belt" not in normandy_ids
    assert "batumi_black_sea_cap" not in normandy_ids
    assert "incirlik_iskenderun_cap" not in normandy_ids
    assert "nellis_north_range_cap" not in normandy_ids
    assert "mount_pleasant_south_atlantic_cap" not in normandy_ids
    assert "needs_oar_point_home" in normandy_ids
    assert "cherbourg_channel_cap" in normandy_ids
    assert "maupertus_inland_strike" in normandy_ids
    caucasus = list_mission_options(theatre="Caucasus", db_path=db)
    assert caucasus["ok"] is True
    caucasus_ids = {o["id"] for o in caucasus["options"] if o["family"] == "channel_place"}
    assert "manston_home" not in caucasus_ids
    assert "cherbourg_channel_cap" not in caucasus_ids
    assert "batumi_home" in caucasus_ids
    assert "batumi_black_sea_cap" in caucasus_ids
    assert "kutaisi_inland_strike" in caucasus_ids
    assert "incirlik_home" not in caucasus_ids
    syria = list_mission_options(theatre="Syria", db_path=db)
    assert syria["ok"] is True
    syria_ids = {o["id"] for o in syria["options"] if o["family"] == "channel_place"}
    assert "incirlik_home" in syria_ids
    assert "incirlik_iskenderun_cap" in syria_ids
    assert "aleppo_inland_strike" in syria_ids
    assert "manston_home" not in syria_ids
    assert "cherbourg_channel_cap" not in syria_ids
    assert "batumi_home" not in syria_ids
    assert "batumi_black_sea_cap" not in syria_ids
    nevada = list_mission_options(theatre="Nevada", db_path=db)
    assert nevada["ok"] is True
    nevada_ids = {o["id"] for o in nevada["options"] if o["family"] == "channel_place"}
    assert "nellis_home" in nevada_ids
    assert "nellis_north_range_cap" in nevada_ids
    assert "creech_range_strike" in nevada_ids
    assert "manston_home" not in nevada_ids
    assert "incirlik_iskenderun_cap" not in nevada_ids
    assert "batumi_black_sea_cap" not in nevada_ids
    assert "mount_pleasant_home" not in nevada_ids
    assert "mount_pleasant_south_atlantic_cap" not in nevada_ids
    falklands = list_mission_options(theatre="Falklands", db_path=db)
    assert falklands["ok"] is True
    falklands_ids = {o["id"] for o in falklands["options"] if o["family"] == "channel_place"}
    assert "mount_pleasant_home" in falklands_ids
    assert "mount_pleasant_south_atlantic_cap" in falklands_ids
    assert "east_falkland_inland_strike" in falklands_ids
    assert "manston_home" not in falklands_ids
    assert "nellis_home" not in falklands_ids
    assert "nellis_north_range_cap" not in falklands_ids
    assert "incirlik_iskenderun_cap" not in falklands_ids
    assert "batumi_black_sea_cap" not in falklands_ids
    all_rows = list_mission_options(db_path=db)
    all_ids = {o["id"] for o in all_rows["options"] if o["family"] == "channel_place"}
    assert "manston_home" in all_ids
    assert "cherbourg_channel_cap" in all_ids
    assert "maupertus_inland_strike" in all_ids
    assert "batumi_black_sea_cap" in all_ids
    assert "kutaisi_inland_strike" in all_ids
    assert "incirlik_iskenderun_cap" in all_ids
    assert "aleppo_inland_strike" in all_ids
    assert "nellis_home" in all_ids
    assert "nellis_north_range_cap" in all_ids
    assert "creech_range_strike" in all_ids
    assert "mount_pleasant_home" in all_ids
    assert "mount_pleasant_south_atlantic_cap" in all_ids
    assert "east_falkland_inland_strike" in all_ids


def test_strike_units_era_and_channel_tag(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    snap = CatalogService(db_path=db).sync()
    blitz = next(u for u in snap.strike_units if u.unit_id == "Blitz_36-6700A")
    assert blitz.era_id == "wwii"
    assert blitz.theatre_id == "TheChannel"
    channel = list_strike_targets(theatre="TheChannel", db_path=db)
    assert channel["ok"] is True
    assert any(u["unit_id"] == "Blitz_36-6700A" for u in channel["units"])
    empty = list_strike_targets(theatre="Normandy", db_path=db)
    assert empty["ok"] is True
    assert any(u["unit_id"] == "Blitz_36-6700A" for u in empty["units"])
    assert any(u["unit_id"] == "flak18" for u in empty["units"])
    assert all(u["domain"] == "land" for u in empty["units"])
    assert not any(u["domain"] == "sea" for u in empty["units"])
    caucasus = list_strike_targets(theatre="Caucasus", db_path=db)
    assert caucasus["ok"] is True
    caucasus_ids = {u["unit_id"] for u in caucasus["units"]}
    assert "Ural-375" in caucasus_ids
    assert "GAZ-66" in caucasus_ids
    assert "ZIL-135" in caucasus_ids
    assert "Blitz_36-6700A" not in caucasus_ids
    assert all(u["domain"] == "land" for u in caucasus["units"])
    ural = next(u for u in snap.strike_units if u.unit_id == "Ural-375")
    assert ural.era_id == "modern"
    assert ural.theatre_id == "Caucasus"
    channel_ids = {u["unit_id"] for u in channel["units"]}
    assert "Ural-375" not in channel_ids
    syria = list_strike_targets(theatre="Syria", db_path=db)
    assert syria["ok"] is True
    syria_ids = {u["unit_id"] for u in syria["units"]}
    assert "Ural-375" in syria_ids
    assert "GAZ-66" in syria_ids
    assert "ZIL-135" in syria_ids
    assert "Blitz_36-6700A" not in syria_ids
    assert all(u["domain"] == "land" for u in syria["units"])
    nevada = list_strike_targets(theatre="Nevada", db_path=db)
    assert nevada["ok"] is True
    nevada_ids = {u["unit_id"] for u in nevada["units"]}
    assert "Ural-375" in nevada_ids
    assert "GAZ-66" in nevada_ids
    assert "ZIL-135" in nevada_ids
    assert "Blitz_36-6700A" not in nevada_ids
    assert all(u["domain"] == "land" for u in nevada["units"])
    falklands = list_strike_targets(theatre="Falklands", db_path=db)
    assert falklands["ok"] is True
    falklands_ids = {u["unit_id"] for u in falklands["units"]}
    assert "Ural-375" in falklands_ids
    assert "GAZ-66" in falklands_ids
    assert "ZIL-135" in falklands_ids
    assert "Blitz_36-6700A" not in falklands_ids
    assert all(u["domain"] == "land" for u in falklands["units"])


def test_metar_egmh_channel_only() -> None:
    channel = ensure_weather_seed(load_mission_spec(MANSTON_FF), seed=1)
    metar_c = format_synthetic_metar(resolve_weather_snapshot(channel), channel)
    assert metar_c.startswith("EGMH ")
    assert metar_c.endswith("NOSIG RMK SIM")
    normandy = ensure_weather_seed(load_mission_spec(NORMANDY_FF), seed=1)
    metar_n = format_synthetic_metar(resolve_weather_snapshot(normandy), normandy)
    assert "EGMH" not in metar_n
    assert "ICAO" not in metar_n
    assert metar_n.endswith("NOSIG RMK SIM")
    caucasus = ensure_weather_seed(load_mission_spec(CAUCASUS_FF), seed=1)
    metar_k = format_synthetic_metar(resolve_weather_snapshot(caucasus), caucasus)
    assert "EGMH" not in metar_k
    assert "ICAO" not in metar_k
    assert metar_k.endswith("NOSIG RMK SIM")
    syria = ensure_weather_seed(load_mission_spec(SYRIA_FF), seed=1)
    metar_s = format_synthetic_metar(resolve_weather_snapshot(syria), syria)
    assert "EGMH" not in metar_s
    assert "ICAO" not in metar_s
    assert metar_s.endswith("NOSIG RMK SIM")
    nevada = ensure_weather_seed(load_mission_spec(NEVADA_FF), seed=1)
    metar_nv = format_synthetic_metar(resolve_weather_snapshot(nevada), nevada)
    assert "EGMH" not in metar_nv
    assert "ICAO" not in metar_nv
    assert metar_nv.endswith("NOSIG RMK SIM")
    falklands = ensure_weather_seed(load_mission_spec(FALKLANDS_FF), seed=1)
    metar_fk = format_synthetic_metar(resolve_weather_snapshot(falklands), falklands)
    assert "EGMH" not in metar_fk
    assert "ICAO" not in metar_fk
    assert metar_fk.endswith("NOSIG RMK SIM")


def test_miz_patch_reweather_fail_closed_on_normandy(tmp_path: Path) -> None:
    miz = compile_needs_oar_point(tmp_path / "nop.miz")
    with zipfile.ZipFile(miz) as z:
        assert "Normandy" in z.read("theatre").decode("utf-8")
    with pytest.raises(ReweatherError, match="TheChannel"):
        reweather_mission(miz, "rain_overcast", seed=3, inventory=_inv())


def test_date_realism_from_era_map() -> None:
    channel = load_mission_spec(MANSTON_FF).model_copy(
        update={"date": load_mission_spec(MANSTON_FF).date.model_copy(update={"year": 2023})}
    )
    warn_c = date_realism_warnings(channel)
    assert warn_c and "2023" in warn_c[0]
    normandy = load_mission_spec(NORMANDY_FF).model_copy(
        update={"date": load_mission_spec(NORMANDY_FF).date.model_copy(update={"year": 2023})}
    )
    warn_n = date_realism_warnings(normandy)
    assert warn_n and "2023" in warn_n[0]
    wwii = load_mission_spec(NORMANDY_FF)
    assert date_realism_warnings(wwii) == ()
    caucasus = load_mission_spec(CAUCASUS_FF)
    assert date_realism_warnings(caucasus) == ()
    syria = load_mission_spec(SYRIA_FF)
    assert date_realism_warnings(syria) == ()
    nevada = load_mission_spec(NEVADA_FF)
    assert date_realism_warnings(nevada) == ()
    falklands = load_mission_spec(FALKLANDS_FF)
    assert date_realism_warnings(falklands) == ()


def test_normandy_join_up_still_compiles(tmp_path: Path) -> None:
    from dcs_miz_planner.models import PlayerFlight, PlayerFlightRole

    spec = load_mission_spec(NORMANDY_FF)
    spec = spec.model_copy(
        update={
            "player": spec.player.model_copy(
                update={
                    "flight": PlayerFlight(
                        size=2, role=PlayerFlightRole.WINGMAN, join_up=True, ai_skill="Average"
                    )
                }
            )
        }
    )
    out = PyDCSCompiler(inventory=_inv()).compile(spec, tmp_path / "nop_join.miz")
    assert out.is_file()
