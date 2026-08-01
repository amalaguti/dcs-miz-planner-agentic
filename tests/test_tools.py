"""Agent tools surface: catalog lookups + validate/compile wrappers."""

from __future__ import annotations

from pathlib import Path

import pytest
from fixtures_support import EXAMPLE_SPEC, channel_available_inventory

from dcs_miz_planner.catalog import CatalogService
from dcs_miz_planner.install.models import AvailabilityState, TheatreInventory, TheatreRecord
from dcs_miz_planner.install.store import InventoryStore
from dcs_miz_planner.tools import (
    compile_mission,
    find_airfield,
    get_aircraft_details,
    get_user_prefs,
    list_generation_history,
    list_mission_options,
    record_feedback,
    record_generation,
    research_guidance,
    set_user_prefs,
    validate_mission_spec,
)


def test_tools_export_surface() -> None:
    assert callable(find_airfield)
    assert callable(get_aircraft_details)
    assert callable(list_mission_options)
    assert callable(validate_mission_spec)
    assert callable(compile_mission)
    assert callable(get_user_prefs)
    assert callable(set_user_prefs)
    assert callable(record_generation)
    assert callable(record_feedback)
    assert callable(list_generation_history)
    assert callable(research_guidance)


def test_find_airfield_manston(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    result = find_airfield("manston", db_path=db)
    assert result["ok"] is True
    names = {a["name"] for a in result["airfields"]}
    assert "Manston" in names
    manston = next(a for a in result["airfields"] if a["name"] == "Manston")
    assert manston["airdrome_id"] == 5


def test_get_aircraft_details_spitfire(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    result = get_aircraft_details("SpitfireLFMkIX", db_path=db)
    assert result["ok"] is True
    assert result["aircraft_id"] == "SpitfireLFMkIX"
    assert result["radio_mhz"] == 124.0


def test_get_aircraft_details_unknown(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    result = get_aircraft_details("NotARealPlane", db_path=db)
    assert result["ok"] is False
    assert result["code"] == "not_found"


def test_list_mission_options_includes_types_and_offerable(tmp_path: Path) -> None:
    from datetime import UTC, datetime

    db = tmp_path / "inventory.sqlite"
    CatalogService(db_path=db).sync()
    InventoryStore(db).replace(
        TheatreInventory(
            scanned_at=datetime(2026, 8, 1, tzinfo=UTC),
            dcs_roots=("C:/FakeDCS",),
            saved_games_roots=(),
            theatres=(
                TheatreRecord(
                    theatre_id="TheChannel",
                    update_id="THECHANNEL_terrain",
                    dcs_root="C:/FakeDCS",
                    state=AvailabilityState.AVAILABLE,
                    planner_supported=True,
                ),
            ),
        )
    )
    CatalogService(db_path=db).ensure_synced()
    result = list_mission_options(db_path=db)
    assert result["ok"] is True
    assert "free_flight" in result["mission_types"]
    assert "intercept" in result["mission_types"]
    assert "cap" in result["mission_types"]
    offerable_ids = {t["theatre_id"] for t in result["offerable_theatres"]}
    assert "TheChannel" in offerable_ids
    options = result["options"]
    assert options
    by_key = {(o["family"], o["id"]): o for o in options}
    assert by_key[("weather", "sunny_clear")]["support"] == "supported"
    assert by_key[("time_of_day", "dawn")]["support"] == "advisory"
    assert by_key[("time_of_day", "dawn")]["meta"]["start_time"] == "06:00"
    assert by_key[("roe_seed", "weapons_hold")]["support"] == "supported"
    assert by_key[("mission_type", "cap")]["support"] == "supported"
    supports = {o["support"] for o in options}
    assert supports >= {"supported", "advisory", "future"}


def test_validate_and_compile_manston(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    validated = validate_mission_spec(EXAMPLE_SPEC, inventory=inv)
    assert validated["ok"] is True

    out = tmp_path / "tools_manston.miz"
    compiled = compile_mission(EXAMPLE_SPEC, out, inventory=inv)
    assert compiled["ok"] is True
    assert Path(compiled["output"]).is_file()


def test_user_memory_tools(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    empty = get_user_prefs(db_path=db)
    assert empty["ok"] is True
    assert empty["prefs"] == {}

    written = set_user_prefs({"preferred_airfield": "Manston"}, db_path=db)
    assert written["ok"] is True
    assert written["prefs"]["preferred_airfield"] == "Manston"

    gid = record_generation(
        outcome="success",
        prompt="test",
        mission_type="free_flight",
        theatre="TheChannel",
        spec_path="out/x.yaml",
        db_path=db,
    )
    assert gid["ok"] is True
    hist = list_generation_history(db_path=db)
    assert hist["ok"] is True
    assert hist["generations"][0]["id"] == gid["generation_id"]

    fb = record_feedback(
        score=4,
        note="solid",
        generation_id=gid["generation_id"],
        source="cli",
        db_path=db,
    )
    assert fb["ok"] is True


def test_research_guidance_offline_notes() -> None:
    result = research_guidance(
        "Channel Spitfire intercept vs Bf-109",
        mission_type="intercept",
        live=False,
    )
    assert result["ok"] is True
    assert result["notes"]
    assert any(
        "intercept" in n["snippet"].lower() or "bounce" in n["snippet"].lower()
        for n in result["notes"]
    )


def test_research_guidance_soft_fails_on_live_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner.tools import research as research_mod

    def boom(_query: str) -> list:
        raise TimeoutError("simulated")

    notes, warning = research_mod.gather_research_notes(
        "tactics",
        mission_type="free_flight",
        live=True,
        web_fetch=boom,
    )
    assert notes
    assert warning is not None
    assert "failed" in warning.lower()
    # Tool surface still ok.
    monkeypatch.setenv("DCS_MIZ_RESEARCH_LIVE", "0")
    tool = research_guidance("free flight procedures", mission_type="free_flight", live=False)
    assert tool["ok"] is True


def test_dispatch_research_guidance() -> None:
    from dcs_miz_planner.agent.tool_bridge import dispatch_tool

    result = dispatch_tool(
        "research_guidance",
        {"query": "Spitfire procedures", "mission_type": "free_flight"},
    )
    assert result["ok"] is True
    assert result["notes"]
