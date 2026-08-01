"""NL→Spec agent: stub planner, tool bridge, live config."""

from __future__ import annotations

from pathlib import Path

import pytest
from fixtures_support import channel_available_inventory

from dcs_miz_planner.agent import (
    AgentConfigError,
    StubLLM,
    live_llm_from_env,
    plan_mission,
    stub_with_find_airfield_then_spec,
    stub_with_get_user_prefs_then_spec,
    stub_with_research_guidance_then_spec,
)
from dcs_miz_planner.agent.tool_bridge import dispatch_tool
from dcs_miz_planner.cli import main
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec
from dcs_miz_planner.memory import OUTCOME_SUCCESS, UserMemoryService


def test_dispatch_find_airfield() -> None:
    result = dispatch_tool("find_airfield", {"query": "Manston"})
    assert result["ok"] is True
    assert any(a["name"] == "Manston" for a in result["airfields"])


def test_stub_plan_writes_valid_yaml(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    db = tmp_path / "inventory.sqlite"
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "cold Spitfire free flight at Manston sunny 09:00",
        out,
        llm=StubLLM(),
        inventory=inv,
        db_path=db,
        voice="raf",
    )
    assert result.ok is True
    assert out.is_file()
    assert result.warnings == ()
    assert result.generation_id is not None
    assert result.voice == "raf"
    assert result.system_prompt is not None
    assert "RAF squadron commander" in result.system_prompt
    assert result.brief is not None
    assert "## Tactics" in result.brief
    assert "## Procedures" in result.brief
    assert "## Watch-outs" in result.brief
    hist = UserMemoryService(db_path=db).list_generations()
    assert len(hist) == 1
    assert hist[0].outcome == OUTCOME_SUCCESS
    assert hist[0].spec_path == str(out)
    spec = load_mission_spec(out)
    assert spec.player.airfield == "Manston"
    assert spec.player.aircraft == "SpitfireLFMkIX"
    miz = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "planned.miz")
    assert miz.is_file()


def test_stub_plan_usaaf_voice(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    out = tmp_path / "usaaf.yaml"
    result = plan_mission(
        "Manston free flight",
        out,
        llm=StubLLM(),
        inventory=inv,
        db_path=tmp_path / "inventory.sqlite",
        voice="usaaf",
    )
    assert result.ok is True
    assert result.voice == "usaaf"
    assert result.system_prompt is not None
    assert "USAAF" in result.system_prompt
    assert result.brief is not None
    assert "Listen up" in result.brief or "skipper" in result.brief.lower()
    assert load_mission_spec(out).player.airfield == "Manston"


def test_modern_date_emits_realism_warning(tmp_path: Path) -> None:
    import json

    from dcs_miz_planner.agent.llm import MANSTON_FREE_FLIGHT_JSON, LLMResponse

    modern = json.loads(MANSTON_FREE_FLIGHT_JSON)
    modern["date"] = {"year": 2023, "month": 10, "day": 1}
    inv = channel_available_inventory()
    out = tmp_path / "modern.yaml"
    result = plan_mission(
        "Manston free flight",
        out,
        llm=StubLLM(script=[LLMResponse(content=json.dumps(modern))]),
        inventory=inv,
        db_path=tmp_path / "inventory.sqlite",
    )
    assert result.ok is True
    assert len(result.warnings) == 1
    assert "2023" in result.warnings[0]
    assert "historical backdrop" in result.warnings[0].lower() or "WWII" in result.warnings[0]
    assert "modern" in result.warnings[0].lower()


def test_stub_tool_call_then_spec(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    out = tmp_path / "via_tools.yaml"
    result = plan_mission(
        "Manston freeflight",
        out,
        llm=stub_with_find_airfield_then_spec(),
        inventory=inv,
        db_path=tmp_path / "inventory.sqlite",
    )
    assert result.ok is True
    assert result.spec is not None
    assert result.spec.theatre == "TheChannel"


def test_stub_get_user_prefs_then_spec(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    db = tmp_path / "inventory.sqlite"
    UserMemoryService(db_path=db).set_prefs({"preferred_airfield": "Manston"})
    out = tmp_path / "via_prefs.yaml"
    result = plan_mission(
        "free flight",
        out,
        llm=stub_with_get_user_prefs_then_spec(),
        inventory=inv,
        db_path=db,
    )
    assert result.ok is True
    assert result.generation_id is not None
    # Bridge returned real prefs during the tool turn (exercise path).
    assert dispatch_tool("get_user_prefs", {}, db_path=db)["prefs"]["preferred_airfield"] == (
        "Manston"
    )


def test_stub_research_guidance_then_spec(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    out = tmp_path / "via_research.yaml"
    result = plan_mission(
        "Manston free flight",
        out,
        llm=stub_with_research_guidance_then_spec(),
        inventory=inv,
        db_path=tmp_path / "inventory.sqlite",
    )
    assert result.ok is True
    assert result.brief is not None
    assert "## Tactics" in result.brief


def test_live_llm_from_env_missing_key() -> None:
    with pytest.raises(AgentConfigError, match="OPENAI_API_KEY"):
        live_llm_from_env(env={})


def test_cli_plan_stub(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    inv = channel_available_inventory()
    monkeypatch.setattr(
        "dcs_miz_planner.validation.get_inventory",
        lambda **_kwargs: inv,
    )
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    out = tmp_path / "cli_planned.yaml"
    db = tmp_path / "inventory.sqlite"
    assert (
        main(
            [
                "plan",
                "Manston free flight",
                "--stub",
                "--voice",
                "raf",
                "-o",
                str(out),
                "--db",
                str(db),
            ]
        )
        == 0
    )
    assert out.is_file()
    assert load_mission_spec(out).player.airfield == "Manston"
    assert main(["prefs", "history", "--db", str(db), "--json"]) == 0


def test_cli_prefs_and_feedback(tmp_path: Path) -> None:
    db = tmp_path / "inventory.sqlite"
    assert main(["prefs", "set", "preferred_airfield", "Manston", "--db", str(db)]) == 0
    assert main(["prefs", "list", "--db", str(db), "--json"]) == 0
    assert main(["feedback", "--score", "5", "--note", "nice", "--db", str(db)]) == 0


def test_cli_plan_live_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rc = main(["plan", "Manston free flight", "-o", "out/should_not_write.yaml"])
    assert rc == 2
