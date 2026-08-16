"""Interactive plan chat / REPL tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent import PlanSession, stub_chat_clarify_then_spec
from dcs_miz_planner.agent.llm import MANSTON_FREE_FLIGHT_JSON, LLMResponse, StubLLM
from dcs_miz_planner.catalog import CatalogService


def test_chat_clarify_tool_accept(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner.tools import research as research_mod

    # Keep multi-turn chat offline-fast: soft-fail live with fixtures.
    monkeypatch.setattr(research_mod, "_live_web_notes", lambda _q: [])

    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    session = PlanSession(
        llm=stub_chat_clarify_then_spec(),
        output_path=out,
        db_path=db,
        inventory=channel_available_inventory(),
        voice="raf",
    )
    session.start()

    r1 = session.handle_line("I'd like something from Manston")
    assert "Manston" in r1.output or "Free flight" in r1.output or "CAP" in r1.output

    r2 = session.handle_line("free flight please")
    assert "schema_version" in r2.output or "Draft Spec" in r2.output
    assert session.proposed_spec is not None

    brief_empty_ok = session.handle_line("/briefing")
    assert "## Tactics" in brief_empty_ok.output or "Free flight" in brief_empty_ok.output

    research = session.handle_line("/research Channel Spitfire weather")
    assert "Research" in research.output
    assert "-" in research.output
    assert "fixture" in research.output.lower()
    assert "Warning:" in research.output

    catalog = session.handle_line("/catalog")
    assert "catalog" in catalog.output.lower() or "mission_types" in catalog.output
    assert "SpitfireLFMkIX" in catalog.output or "sunny_clear" in catalog.output

    accepted = session.handle_line("/accept")
    assert out.is_file()
    assert "Wrote Spec" in accepted.output
    assert "## Tactics" in accepted.output


def test_chat_research_labels_live_soft_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from dcs_miz_planner.tools import research as research_mod

    monkeypatch.setattr(research_mod, "_live_web_notes", lambda _q: [])
    session = PlanSession(
        llm=StubLLM(),
        output_path=tmp_path / "x.yaml",
        inventory=channel_available_inventory(),
    )
    session.start()
    r = session.handle_line("/research Manston spitfire")
    assert "Warning:" in r.output
    assert "Offline fixture fallback" in r.output or "fixture fallback" in r.output.lower()
    injected = session.messages[-2]["content"]
    assert "<<<UNTRUSTED_RESEARCH_NOTES>>>" in injected
    assert "<<<END_UNTRUSTED_RESEARCH_NOTES>>>" in injected
    assert "UNTRUSTED" in injected
    assert "Spec" in injected


def test_chat_no_auto_write_without_accept(tmp_path: Path) -> None:
    db = tmp_path / "inv.sqlite"
    CatalogService(db_path=db).ensure_synced()
    out = tmp_path / "planned.yaml"
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=MANSTON_FREE_FLIGHT_JSON)]),
        output_path=out,
        db_path=db,
        inventory=channel_available_inventory(),
    )
    session.start()
    session.handle_line("give me the Spec")
    assert session.proposed_spec is not None
    assert not out.exists()


def test_briefing_without_draft(tmp_path: Path) -> None:
    session = PlanSession(
        llm=StubLLM(),
        output_path=tmp_path / "x.yaml",
        inventory=channel_available_inventory(),
    )
    session.start()
    r = session.handle_line("/briefing")
    assert "No draft" in r.output


def test_help_lists_new_commands(tmp_path: Path) -> None:
    session = PlanSession(llm=StubLLM(), output_path=tmp_path / "x.yaml")
    session.start()
    r = session.handle_line("/help")
    assert "/briefing" in r.output
    assert "/research" in r.output
    assert "/catalog" in r.output


def test_verbose_defaults_off(tmp_path: Path) -> None:
    from dcs_miz_planner.agent.verbose import DEFAULT_VERBOSE

    assert DEFAULT_VERBOSE is False
    session = PlanSession(llm=StubLLM(), output_path=tmp_path / "x.yaml")
    banner = session.start()
    assert "verbose=off" in banner
    assert session.verbose is False


def test_verbose_slash_toggle(tmp_path: Path) -> None:
    session = PlanSession(llm=StubLLM(), output_path=tmp_path / "x.yaml", verbose=True)
    banner = session.start()
    assert "verbose=on" in banner
    r = session.handle_line("/verbose off")
    assert session.verbose is False
    assert "off" in r.output
    session.handle_line("/verbose on")
    assert session.verbose is True


def test_compose_chat_mode() -> None:
    from dcs_miz_planner.agent.prompts import compose_system_prompt

    prompt = compose_system_prompt("raf", mode="chat")
    assert "/accept" in prompt
    assert "Interactive chat" in prompt
    assert "get_mission_spec_schema" in prompt
    assert "nested player" in prompt or "player{}" in prompt
    assert "Anti-patterns" in prompt or "anti-pattern" in prompt.lower()


def test_host_spec_repair_nudge_includes_derived_example() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    nudge = host_spec_repair_nudge(
        "theatre Field required",
        rejected_text='{"mission_type": "cap"}',
    )
    assert "theatre Field required" in nudge
    assert "player" in nudge
    assert "TheChannel" in nudge
    assert '"mission_type": "cap"' in nudge or '"mission_type":"cap"' in nudge
    assert "DO NOT emit" in nudge


def test_host_spec_repair_nudge_normandy_cap_not_manston() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    nudge = host_spec_repair_nudge(
        "cap.duration_min Field required",
        rejected_text='{"mission_type": "cap", "theatre": "Normandy"}',
    )
    assert '"theatre": "Normandy"' in nudge or '"theatre":"Normandy"' in nudge
    assert '"airfield": "NeedsOarPoint"' in nudge or '"airfield":"NeedsOarPoint"' in nudge
    assert '"bearing_deg": 180' in nudge or '"bearing_deg":180' in nudge
    assert '"airfield": "Manston"' not in nudge and '"airfield":"Manston"' not in nudge


def test_host_spec_repair_nudge_theatre_kwarg_without_json() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    nudge = host_spec_repair_nudge(
        "Validation failed:\n[]",
        mission_type="cap",
        theatre="Normandy",
    )
    assert '"airfield": "NeedsOarPoint"' in nudge or '"airfield":"NeedsOarPoint"' in nudge
    assert '"airfield": "Manston"' not in nudge and '"airfield":"Manston"' not in nudge


def test_host_spec_repair_nudge_caucasus_domain_uses_batumi() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    nudge = host_spec_repair_nudge(
        'Validation failed:\n[{"code": "domain_unsupported_theatre"}]',
        rejected_text='{"mission_type": "cap", "theatre": "Caucasus"}',
    )
    assert "Batumi" in nudge
    assert "Su-25T" in nudge
    assert '"airfield": "Batumi"' in nudge or '"airfield":"Batumi"' in nudge
    assert '"airfield": "NeedsOarPoint"' not in nudge
    assert '"airfield":"NeedsOarPoint"' not in nudge
    assert '"airfield": "Manston"' not in nudge
    assert '"airfield":"Manston"' not in nudge


def test_host_spec_repair_nudge_needs_oar_point_implies_normandy() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    nudge = host_spec_repair_nudge(
        "theatre Field required",
        rejected_text='{"mission_type": "cap", "player": {"airfield": "NeedsOarPoint"}}',
    )
    assert '"airfield": "NeedsOarPoint"' in nudge or '"airfield":"NeedsOarPoint"' in nudge
    assert '"bearing_deg": 180' in nudge or '"bearing_deg":180' in nudge
    assert '"airfield": "Manston"' not in nudge and '"airfield":"Manston"' not in nudge


def test_host_spec_repair_nudge_domain_mismatch_includes_geometry() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    payload = (
        'Validation failed:\n[{"code": "motion_domain_mismatch", "message": "land path over sea"}]'
    )
    nudge = host_spec_repair_nudge(payload, mission_type="ground_attack")
    assert "motion_domain_mismatch" in nudge or "domain mismatch" in nudge.lower()
    assert "125" in nudge or "french_coast" in nudge
    assert "140" in nudge or "mid_channel" in nudge
    assert "coastal_harbour" in nudge or "68" in nudge or "70" in nudge
    assert "path:" in nudge or "128" in nudge


def test_host_spec_repair_nudge_path_example_on_path_mismatch() -> None:
    from dcs_miz_planner.agent.prompts import host_spec_repair_nudge

    payload = (
        '[{"code": "motion_domain_mismatch", "message": '
        '"Target x is domain land but motion sample path[1] is sea"}]'
    )
    nudge = host_spec_repair_nudge(payload, mission_type="ground_attack")
    assert "bearing_deg: 125" in nudge
    assert "distance_km: 76" in nudge


def test_invalid_embedded_spec_injects_shape_nudge(tmp_path: Path) -> None:
    bad = """Here is the Spec:
{
  "schema_version": "1",
  "mission_type": "cap",
  "date": "1944-06-06",
  "airfield": "Manston",
  "aircraft": "SpitfireLFMkIX",
  "enemies": [{"type": "intercept_enemy", "id": "Bf-109K-4"}],
  "cap": {"bearing_deg": 270, "distance_km": 30, "altitude_m": 5000,
          "pattern": "circle", "engagement": "weapons_free",
          "objectives": [{"type": "patrol"}]}
}
"""
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=bad)]),
        output_path=tmp_path / "planned.yaml",
        inventory=channel_available_inventory(),
    )
    session.start()
    r = session.handle_line("ready")
    assert "NOT captured" in r.output
    assert session.proposed_spec is None
    assert session.last_spec_error
    # Host injected a repair nudge with the derived CAP example into history.
    assert any(
        "derived example" in (m.get("content") or "").lower()
        or "Mission Spec example for mission_type='cap'" in (m.get("content") or "")
        for m in session.messages
        if m.get("role") == "user"
    )


def test_valid_embedded_spec_captured(tmp_path: Path) -> None:
    wrapped = (
        "Here is the finalized Spec:\n\n"
        + MANSTON_FREE_FLIGHT_JSON
        + "\n\nType /accept when ready."
    )
    session = PlanSession(
        llm=StubLLM(script=[LLMResponse(content=wrapped)]),
        output_path=tmp_path / "planned.yaml",
        inventory=channel_available_inventory(),
    )
    session.start()
    r = session.handle_line("lock it in")
    assert "Draft Spec captured" in r.output
    assert session.proposed_spec is not None
    accepted = session.handle_line("/accept")
    assert "Wrote Spec" in accepted.output
    assert (tmp_path / "planned.yaml").is_file()
