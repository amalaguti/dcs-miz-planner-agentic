"""Agent tools surface: catalog lookups + validate/compile wrappers."""

from __future__ import annotations

import json
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
    get_mission_spec_schema,
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
    assert callable(get_mission_spec_schema)
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
    assert "ground_attack" in result["mission_types"]
    assert "escort" in result["mission_types"]
    offerable_ids = {t["theatre_id"] for t in result["offerable_theatres"]}
    assert "TheChannel" in offerable_ids
    options = result["options"]
    assert options
    by_key = {(o["family"], o["id"]): o for o in options}
    assert by_key[("weather", "sunny_clear")]["support"] == "supported"
    assert by_key[("weather", "dawn_clear")]["support"] == "supported"
    assert by_key[("weather", "marginal_vfr")]["support"] == "supported"
    assert by_key[("time_of_day", "dawn")]["support"] == "advisory"
    assert by_key[("time_of_day", "dawn")]["meta"]["start_time"] == "06:00"
    assert by_key[("roe_seed", "weapons_hold")]["support"] == "supported"
    assert by_key[("randomization", "seeded_reroll")]["support"] == "advisory"
    assert by_key[("mission_type", "cap")]["support"] == "supported"
    assert by_key[("mission_type", "ground_attack")]["support"] == "supported"
    assert by_key[("mission_type", "escort")]["support"] == "supported"
    assert by_key[("payload_family", "spitfire_2x250_slipper")]["support"] == "supported"
    assert by_key[("payload_family", "spitfire_2x250_slipper")]["meta"]["payload"] == (
        "spitfire_2x250_slipper"
    )
    # mission_behaviour / mission_inspiration capability catalog
    assert by_key[("mission_behaviour", "altitude_speed_gates")]["support"] == "supported"
    assert "unit_altitude_higher" in str(
        by_key[("mission_behaviour", "altitude_speed_gates")]["meta"]
    )
    assert by_key[("mission_behaviour", "mark_smoke")]["support"] == "supported"
    assert by_key[("mission_behaviour", "narrative_pack")]["support"] == "supported"
    assert by_key[("mission_behaviour", "radio_late_activation")]["support"] == "supported"
    assert by_key[("mission_behaviour", "sound_flag_chain")]["support"] == "supported"
    assert by_key[("mission_behaviour", "group_life_less")]["support"] == "supported"

    # Mission-designer shelves (#30e)
    for mode in ("fixed", "live", "choose", "hybrid"):
        row = by_key[("dynamics_mode", mode)]
        assert row["support"] == "advisory"
        assert row["meta"].get("layer") == "play_time"
    soft = by_key[("strike_target_class", "soft_vehicles")]
    assert soft["support"] == "supported"
    assert soft["meta"]["domain"] == "land"
    assert "Blitz_36-6700A" in soft["meta"]["unit_ids"]
    sea = by_key[("strike_target_class", "sea_craft")]
    assert sea["meta"]["domain"] == "sea"
    assert "Schnellboot_type_S130" in sea["meta"]["ship_ids"]
    assert by_key[("strike_target_class", "hard_infrastructure")]["support"] == "future"
    assert by_key[("channel_place", "manston_home")]["meta"]["airfield"] == "Manston"
    assert by_key[("channel_place", "french_coast_strike_belt")]["meta"]["domain"] == "land"
    assert by_key[("channel_place", "mid_channel_shipping")]["meta"]["domain"] == "sea"
    insp = by_key[("mission_inspiration", "low_level_channel_hop")]
    assert insp["support"] == "advisory"
    assert "altitude_speed_gates" in insp["meta"]["behaviours"]
    supports = {o["support"] for o in options}
    assert supports >= {"supported", "advisory"}
    assert "future" not in {
        by_key[("payload_family", pid)]["support"]
        for pid in ("spitfire_2x250_slipper", "spitfire_2x250", "spitfire_1x500")
    }


def test_validate_and_compile_manston(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    validated = validate_mission_spec(EXAMPLE_SPEC, inventory=inv)
    assert validated["ok"] is True

    out = tmp_path / "tools_manston.miz"
    compiled = compile_mission(EXAMPLE_SPEC, out, inventory=inv, out_root=tmp_path)
    assert compiled["ok"] is True
    assert Path(compiled["output"]).is_file()


def test_compile_outside_out_rejected(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    allowed = tmp_path / "out"
    allowed.mkdir()
    outside = tmp_path / "elsewhere" / "nope.miz"
    outside.parent.mkdir()
    result = compile_mission(EXAMPLE_SPEC, outside, inventory=inv, out_root=allowed)
    assert result["ok"] is False
    assert result["code"] == "path_not_allowed"
    assert not outside.exists()


def test_dispatch_blocks_mutating_tools_by_default() -> None:
    from dcs_miz_planner.agent.tool_bridge import (
        MUTATING_TOOL_NAMES,
        TOOL_DEFINITIONS,
        dispatch_tool,
    )

    names = {t["function"]["name"] for t in TOOL_DEFINITIONS}
    assert "compile_mission" not in names
    assert "set_user_prefs" not in names
    for name in MUTATING_TOOL_NAMES:
        result = dispatch_tool(name, {})
        assert result["ok"] is False
        assert result["code"] == "mutating_tool_blocked"


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


def test_enrich_live_query_adds_context() -> None:
    from dcs_miz_planner.tools.research import enrich_live_query

    enriched = enrich_live_query(
        "dawn patrol weather",
        mission_type="cap",
        theatre="TheChannel",
        aircraft="SpitfireLFMkIX",
    )
    assert "dawn patrol weather" in enriched
    assert "cap" in enriched.lower()
    assert "TheChannel" in enriched
    assert "SpitfireLFMkIX" in enriched
    assert "WWII" in enriched


def test_enrich_live_query_mission_design_focus() -> None:
    from dcs_miz_planner.tools.research import enrich_live_query

    enriched = enrich_live_query(
        "Spitfire low level Channel mission ideas",
        mission_type="free_flight",
        theatre="TheChannel",
        focus="mission_design",
    )
    lower = enriched.lower()
    assert "user files" in lower
    assert "mission editor" in lower or "triggers" in lower
    assert "github" in lower or "miz" in lower


def test_research_guidance_passes_focus(monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner.tools import research as research_mod
    from dcs_miz_planner.tools.surface import research_guidance

    seen: dict[str, str | None] = {}

    def fake_gather(query, **kwargs):  # type: ignore[no-untyped-def]
        seen["focus"] = kwargs.get("focus")
        return ([{"title": "t", "snippet": "s", "source": "fixture:x"}], None)

    monkeypatch.setattr(research_mod, "gather_research_notes", fake_gather)
    # surface imports gather at module level — patch surface binding too
    import dcs_miz_planner.tools.surface as surface_mod

    monkeypatch.setattr(surface_mod, "gather_research_notes", fake_gather)
    result = research_guidance("design a strike", focus="mission_design")
    assert result["ok"] is True
    assert result.get("focus") == "mission_design"
    assert seen["focus"] == "mission_design"


def test_research_guidance_live_success_via_inject() -> None:
    from dcs_miz_planner.tools import research as research_mod

    def fake_fetch(_query: str) -> list[dict[str, str]]:
        return [
            {
                "title": "RAF Manston",
                "snippet": "Historic Channel airfield used by Fighter Command.",
                "source": "https://example.test/manston",
            }
        ]

    notes, warning = research_mod.gather_research_notes(
        "Manston spitfire",
        mission_type="free_flight",
        theatre="TheChannel",
        aircraft="SpitfireLFMkIX",
        live=True,
        web_fetch=fake_fetch,
    )
    assert warning is None
    assert notes
    assert any(not research_mod.is_fixture_source(n["source"]) for n in notes)
    assert notes[0]["source"].startswith("https://")


def test_research_guidance_live_empty_soft_fails() -> None:
    from dcs_miz_planner.tools import research as research_mod

    notes, warning = research_mod.gather_research_notes(
        "tactics",
        mission_type="free_flight",
        live=True,
        web_fetch=lambda _q: [],
    )
    assert notes
    assert warning is not None
    assert "no snippets" in warning.lower()
    assert "offline fixtures" in warning.lower()
    assert all(research_mod.is_fixture_source(n["source"]) for n in notes)


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
    assert "offline fixtures" in warning.lower()
    # Tool surface still ok.
    monkeypatch.setenv("DCS_MIZ_RESEARCH_LIVE", "0")
    tool = research_guidance("free flight procedures", mission_type="free_flight", live=False)
    assert tool["ok"] is True


def test_live_cascade_tries_html_when_instant_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner.tools import research as research_mod

    calls: list[str] = []

    def boom_instant(_query: str, *, timeout_s: float = 4.0) -> list:
        calls.append("instant")
        raise json.JSONDecodeError("Expecting value", "", 0)

    def html_ok(query: str, *, timeout_s: float = 6.0) -> list[dict[str, str]]:
        calls.append("html")
        return [
            {
                "title": "Manston",
                "snippet": f"HTML hit for {query}",
                "source": "https://example.test/manston",
            }
        ]

    monkeypatch.setattr(research_mod, "_duckduckgo_instant_notes", boom_instant)
    monkeypatch.setattr(research_mod, "_duckduckgo_html_notes", html_ok)
    notes = research_mod._live_web_notes("Manston spitfire")
    assert calls == ["instant", "html"]
    assert notes and "HTML hit" in notes[0]["snippet"]


def test_duckduckgo_html_parser_extracts_results() -> None:
    from dcs_miz_planner.tools.research import _DuckDuckGoHtmlResultsParser

    sample = """
    <div class="result">
      <a class="result__a" href="/l/?uddg=https%3A%2F%2Fexample.test%2Fspitfire">Spitfire LF Mk IX</a>
      <a class="result__snippet">Supermarine Spitfire fighter used by the RAF.</a>
    </div>
    """
    parser = _DuckDuckGoHtmlResultsParser()
    parser.feed(sample)
    assert parser.results
    assert "Spitfire" in parser.results[0]["title"]
    assert "RAF" in parser.results[0]["snippet"]
    assert "example.test" in parser.results[0]["source"]


def test_dispatch_research_guidance() -> None:
    from dcs_miz_planner.agent.tool_bridge import dispatch_tool

    result = dispatch_tool(
        "research_guidance",
        {"query": "Spitfire procedures", "mission_type": "free_flight"},
    )
    assert result["ok"] is True
    assert result["notes"]


def test_dispatch_list_installed_campaigns() -> None:
    from dcs_miz_planner.agent.tool_bridge import TOOL_DEFINITIONS, dispatch_tool

    names = {t["function"]["name"] for t in TOOL_DEFINITIONS}
    assert "list_installed_campaigns" in names
    result = dispatch_tool("list_installed_campaigns", {})
    assert result["ok"] is True
    assert "campaigns" in result


def test_prompts_mention_capability_catalog() -> None:
    from dcs_miz_planner.agent.prompts import compose_system_prompt
    from dcs_miz_planner.agent.spec_schema import build_spec_schema
    from dcs_miz_planner.agent.tool_bridge import TOOL_DEFINITIONS

    prompt = compose_system_prompt("raf")
    assert "mission_behaviour" in prompt
    assert "mission_inspiration" in prompt
    assert "dynamics_mode" in prompt
    assert "strike_target_class" in prompt
    assert "channel_place" in prompt
    assert "Layer A" in prompt or "randomize" in prompt
    assert "Layer B" in prompt or "play-time" in prompt.lower() or "play-time" in prompt
    assert "list_installed_campaigns" in prompt
    assert "mission_design" in prompt
    assert "briefing themes" not in prompt.lower()
    assert "include_doc_text" in prompt or "Doc/" in prompt
    schema = build_spec_schema("free_flight")
    joined = " ".join(schema.notes)
    assert "mission_behaviour" in joined
    assert "dynamics_mode" in joined
    assert "strike_target_class" in joined
    assert "list_installed_campaigns" in joined
    assert "briefing themes" not in joined.lower()
    options_tool = next(
        t for t in TOOL_DEFINITIONS if t["function"]["name"] == "list_mission_options"
    )
    opt_desc = options_tool["function"]["description"]
    assert "dynamics_mode" in opt_desc
    assert "strike_target_class" in opt_desc
    assert "channel_place" in opt_desc
    camp_tool = next(
        t for t in TOOL_DEFINITIONS if t["function"]["name"] == "list_installed_campaigns"
    )
    desc = camp_tool["function"]["description"].lower()
    assert "briefing themes" not in desc
    assert "filename" in desc
    assert "include_doc_text" in camp_tool["function"]["parameters"]["properties"]
