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
    DomainUnsupportedTheatre,
    airfield_relative_map_point,
    require_channel_domain,
    strike_domain_for_spec,
)
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.intercept_spawn import (
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
INTERCEPT = REPO / "examples" / "manston_dawn_intercept.yaml"
GA = REPO / "examples" / "manston_ground_attack.yaml"
NORMANDY_FF = REPO / "examples" / "needs_oar_point_cold_freeflight.yaml"
NORMANDY_CAP = REPO / "examples" / "needs_oar_point_cap.yaml"
MANSTON_FF = REPO / "examples" / "manston_cold_freeflight.yaml"
CAUCASUS_FF = REPO / "examples" / "batumi_cold_freeflight.yaml"
SYRIA_FF = REPO / "examples" / "incirlik_cold_freeflight.yaml"


def _normandy_intercept_json() -> str:
    """Normandy intercept JSON (Channel geometry copied onto NeedsOarPoint player)."""
    spec = load_mission_spec(INTERCEPT).model_copy(
        update={"theatre": "Normandy", "player": load_mission_spec(NORMANDY_FF).player}
    )
    return spec.model_dump_json()


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
    assert "Germany" not in registry.list_countries()
    assert "Germany" not in known_countries(era="modern")
    assert set(registry.list_countries(era="modern")) == {"Georgia", "Turkey"}


def test_era_for_theatre_wwii() -> None:
    registry = get_channel_registry()
    assert registry.era_for_theatre("TheChannel") == "wwii"
    assert registry.era_for_theatre("Normandy") == "wwii"
    assert registry.era_for_theatre("Caucasus") == "modern"
    assert registry.era_for_theatre("Syria") == "modern"


def test_airfield_relative_map_point_passes_theatre() -> None:
    spec = load_mission_spec(NORMANDY_FF)
    x, y = airfield_relative_map_point(spec, bearing_deg=120.0, distance_km=5.0)
    assert isinstance(x, float)
    assert isinstance(y, float)


def test_domain_fail_closed_on_normandy_strike() -> None:
    spec = load_mission_spec(GA).model_copy(
        update={"theatre": "Normandy", "player": load_mission_spec(NORMANDY_FF).player}
    )
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "domain_unsupported_theatre" for e in result.errors)
    with pytest.raises(DomainUnsupportedTheatre):
        require_channel_domain("Normandy")
    with pytest.raises(DomainUnsupportedTheatre):
        strike_domain_for_spec(spec)


def test_channel_strike_domain_still_classified() -> None:
    spec = load_mission_spec(GA)
    result = validate_mission_spec(spec, inventory=_inv())
    assert result.ok, result.errors
    assert strike_domain_for_spec(spec) == "land"


def test_intercept_fail_closed_on_normandy(tmp_path: Path) -> None:
    player = load_mission_spec(NORMANDY_FF).player
    spec = load_mission_spec(INTERCEPT).model_copy(update={"theatre": "Normandy", "player": player})
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "intercept_unsupported_theatre" for e in result.errors)
    assert not intercept_supported("Normandy")
    out = tmp_path / "should_not_write_normandy_intercept.miz"
    with pytest.raises(ValueError):
        PyDCSCompiler(inventory=_inv()).compile(spec, out)
    assert not out.is_file()


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
    for opt in places:
        if opt.id in {"needs_oar_point_home", "cherbourg_channel_cap"}:
            assert opt.meta.get("theatre") == "Normandy"
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


def test_schema_theatre_syria_combat_no_manston_skeleton() -> None:
    with pytest.raises(ValueError, match="not supported for theatre Syria"):
        build_spec_schema("intercept", theatre="Syria")
    with pytest.raises(ValueError, match="not supported for theatre Syria"):
        build_spec_schema("cap", theatre="Syria")
    tool = get_mission_spec_schema("cap", theatre="Syria")
    assert tool["ok"] is False
    assert tool["code"] == "combat_unsupported_theatre"
    blob = json.dumps(tool)
    assert "Manston" not in blob
    assert "NeedsOarPoint" not in blob
    assert "Batumi" not in blob


def test_schema_theatre_caucasus_combat_no_manston_skeleton() -> None:
    with pytest.raises(ValueError, match="not supported for theatre Caucasus"):
        build_spec_schema("intercept", theatre="Caucasus")
    with pytest.raises(ValueError, match="not supported for theatre Caucasus"):
        build_spec_schema("cap", theatre="Caucasus")
    tool = get_mission_spec_schema("cap", theatre="Caucasus")
    assert tool["ok"] is False
    assert tool["code"] == "combat_unsupported_theatre"
    blob = json.dumps(tool)
    assert "Manston" not in blob
    assert "NeedsOarPoint" not in blob


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
    spec_ac = load_mission_spec(MANSTON_FF).model_copy(
        update={
            "player": load_mission_spec(MANSTON_FF).player.model_copy(update={"aircraft": "Su-25T"})
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert not result_ac.ok
    assert any(e.code == "unknown_aircraft" for e in result_ac.errors)


def test_era_filter_caucasus_rejects_uk_and_spitfire() -> None:
    spec = load_mission_spec(CAUCASUS_FF).model_copy(
        update={
            "player": load_mission_spec(CAUCASUS_FF).player.model_copy(update={"country": "UK"})
        }
    )
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "unknown_country" for e in result.errors)
    spec_ac = load_mission_spec(CAUCASUS_FF).model_copy(
        update={
            "player": load_mission_spec(CAUCASUS_FF).player.model_copy(
                update={"aircraft": "SpitfireLFMkIX"}
            )
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert not result_ac.ok
    assert any(e.code == "unknown_aircraft" for e in result_ac.errors)


def test_era_filter_syria_rejects_uk_and_spitfire() -> None:
    spec = load_mission_spec(SYRIA_FF).model_copy(
        update={"player": load_mission_spec(SYRIA_FF).player.model_copy(update={"country": "UK"})}
    )
    result = validate_mission_spec(spec, inventory=_inv())
    assert not result.ok
    assert any(e.code == "unknown_country" for e in result.errors)
    spec_ac = load_mission_spec(SYRIA_FF).model_copy(
        update={
            "player": load_mission_spec(SYRIA_FF).player.model_copy(
                update={"aircraft": "SpitfireLFMkIX"}
            )
        }
    )
    result_ac = validate_mission_spec(spec_ac, inventory=_inv())
    assert not result_ac.ok
    assert any(e.code == "unknown_aircraft" for e in result_ac.errors)


def test_era_filter_caucasus_georgia_and_syria_turkey_ok() -> None:
    caucasus = load_mission_spec(CAUCASUS_FF)
    assert validate_mission_spec(caucasus, inventory=_inv()).ok
    syria = load_mission_spec(SYRIA_FF)
    assert validate_mission_spec(syria, inventory=_inv()).ok


def test_caucasus_cap_invent_nudge() -> None:
    spec = load_mission_spec(NORMANDY_CAP).model_copy(
        update={"theatre": "Caucasus", "player": load_mission_spec(CAUCASUS_FF).player}
    )
    nudge = host_normandy_combat_nudge(spec)
    assert nudge is not None
    assert "Batumi" in nudge
    assert "free_flight" in nudge
    assert "CAP at NeedsOarPoint" not in nudge
    ff = load_mission_spec(CAUCASUS_FF)
    assert host_normandy_combat_nudge(ff) is None


def test_syria_cap_invent_nudge() -> None:
    spec = load_mission_spec(NORMANDY_CAP).model_copy(
        update={"theatre": "Syria", "player": load_mission_spec(SYRIA_FF).player}
    )
    nudge = host_normandy_combat_nudge(spec)
    assert nudge is not None
    assert "Incirlik" in nudge
    assert "free_flight" in nudge
    assert "CAP at NeedsOarPoint" not in nudge
    assert "free_flight at Batumi" not in nudge
    ff = load_mission_spec(SYRIA_FF)
    assert host_normandy_combat_nudge(ff) is None


def test_schema_theatre_normandy_free_flight() -> None:
    view = build_spec_schema("free_flight", theatre="Normandy")
    assert view.example["theatre"] == "Normandy"
    assert view.example["player"]["airfield"] == "NeedsOarPoint"
    assert view.example["player"]["airfield"] != "Manston"
    tool = get_mission_spec_schema("free_flight", theatre="Normandy")
    assert tool["ok"] is True
    assert tool["example"]["player"]["airfield"] == "NeedsOarPoint"


def test_schema_theatre_normandy_combat_no_manston_skeleton() -> None:
    with pytest.raises(ValueError, match="not supported for theatre Normandy"):
        build_spec_schema("intercept", theatre="Normandy")
    tool = get_mission_spec_schema("ground_attack", theatre="Normandy")
    assert tool["ok"] is False
    assert tool["code"] == "combat_unsupported_theatre"
    blob = json.dumps(tool)
    assert "Manston" not in blob
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


def test_normandy_combat_invent_nudge() -> None:
    spec = load_mission_spec(INTERCEPT).model_copy(
        update={"theatre": "Normandy", "player": load_mission_spec(NORMANDY_FF).player}
    )
    nudge = host_normandy_combat_nudge(spec)
    assert nudge is not None
    assert "NeedsOarPoint" in nudge
    ff = load_mission_spec(NORMANDY_FF)
    assert host_normandy_combat_nudge(ff) is None
    assert host_normandy_combat_nudge(load_mission_spec(NORMANDY_CAP)) is None


def test_chat_second_normandy_combat_json_not_captured(tmp_path: Path) -> None:
    """Combat refuse is every turn — a second intercept JSON must not become the draft."""
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    intercept_json = _normandy_intercept_json()
    session = PlanSession(
        llm=StubLLM(
            script=[
                LLMResponse(content=intercept_json),
                LLMResponse(content=intercept_json),
            ]
        ),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    first = session.handle_line("Normandy intercept")
    assert "Draft NOT captured" in first.output or "not inventable" in first.output.lower()
    assert session.proposed_spec is None
    assert session.draft_spec is None
    second = session.handle_line("still an intercept please")
    assert "Draft NOT captured" in second.output or "not inventable" in second.output.lower()
    assert session.proposed_spec is None
    assert session.draft_spec is None
    accepted = session.handle_line("/accept")
    assert not out.exists()
    assert "Wrote Spec" not in accepted.output


def test_accept_refuses_slipped_normandy_combat_draft(tmp_path: Path) -> None:
    """/accept must not write a Normandy intercept draft that slipped into proposed_spec."""
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    session = PlanSession(
        llm=StubLLM(),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    slipped = load_mission_spec(INTERCEPT).model_copy(
        update={"theatre": "Normandy", "player": load_mission_spec(NORMANDY_FF).player}
    )
    session.proposed_spec = slipped
    session.draft_spec = slipped
    accepted = session.handle_line("/accept")
    assert not out.exists()
    assert "Wrote Spec" not in accepted.output
    assert "not inventable" in accepted.output.lower() or "NOT written" in accepted.output


def test_planner_second_normandy_combat_not_written(tmp_path: Path) -> None:
    """After one combat nudge, a still-intercept Spec must not be written."""
    intercept_json = _normandy_intercept_json()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "Normandy intercept",
        out,
        llm=StubLLM(
            script=[
                LLMResponse(content=intercept_json),
                LLMResponse(content=intercept_json),
            ]
        ),
        inventory=_inv(),
        db_path=tmp_path / "inventory.sqlite",
        max_turns=2,
    )
    assert result.ok is False
    assert not out.exists()
    assert result.spec is None or host_normandy_combat_nudge(result.spec) is not None


def test_chat_caucasus_cap_not_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = (
        load_mission_spec(NORMANDY_CAP)
        .model_copy(update={"theatre": "Caucasus", "player": load_mission_spec(CAUCASUS_FF).player})
        .model_dump_json()
    )
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    first = session.handle_line("Caucasus CAP")
    assert "Draft NOT captured" in first.output or "not inventable" in first.output.lower()
    assert "Batumi" in first.output
    assert "NeedsOarPoint" not in first.output
    assert session.proposed_spec is None
    accepted = session.handle_line("/accept")
    assert not out.exists()
    assert "Wrote Spec" not in accepted.output


def test_chat_syria_cap_not_captured(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    cap_json = (
        load_mission_spec(NORMANDY_CAP)
        .model_copy(update={"theatre": "Syria", "player": load_mission_spec(SYRIA_FF).player})
        .model_dump_json()
    )
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=cap_json)]),
        output_path=out,
        db_path=db,
        inventory=_inv(),
    )
    session.start()
    first = session.handle_line("Syria CAP")
    assert "Draft NOT captured" in first.output or "not inventable" in first.output.lower()
    assert "Incirlik" in first.output
    assert "NeedsOarPoint" not in first.output
    assert "Batumi" not in first.output
    assert session.proposed_spec is None
    accepted = session.handle_line("/accept")
    assert not out.exists()
    assert "Wrote Spec" not in accepted.output


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
    assert "manston_home" in channel_ids
    assert "french_coast_strike_belt" in channel_ids
    assert any(o["family"] == "weather" for o in channel["options"])
    normandy = list_mission_options(theatre="Normandy", db_path=db)
    assert normandy["ok"] is True
    normandy_ids = {o["id"] for o in normandy["options"] if o["family"] == "channel_place"}
    assert "manston_home" not in normandy_ids
    assert "french_coast_strike_belt" not in normandy_ids
    assert "needs_oar_point_home" in normandy_ids
    assert "cherbourg_channel_cap" in normandy_ids
    all_rows = list_mission_options(db_path=db)
    all_ids = {o["id"] for o in all_rows["options"] if o["family"] == "channel_place"}
    assert "manston_home" in all_ids
    assert "cherbourg_channel_cap" in all_ids


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
    assert empty["units"] == []
    caucasus = list_strike_targets(theatre="Caucasus", db_path=db)
    assert caucasus["ok"] is True
    assert caucasus["units"] == []
    syria = list_strike_targets(theatre="Syria", db_path=db)
    assert syria["ok"] is True
    assert syria["units"] == []


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
