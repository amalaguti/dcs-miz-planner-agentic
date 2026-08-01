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
)
from dcs_miz_planner.agent.tool_bridge import dispatch_tool
from dcs_miz_planner.cli import main
from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec


def test_dispatch_find_airfield() -> None:
    result = dispatch_tool("find_airfield", {"query": "Manston"})
    assert result["ok"] is True
    assert any(a["name"] == "Manston" for a in result["airfields"])


def test_stub_plan_writes_valid_yaml(tmp_path: Path) -> None:
    inv = channel_available_inventory()
    out = tmp_path / "planned.yaml"
    result = plan_mission(
        "cold Spitfire free flight at Manston sunny 09:00",
        out,
        llm=StubLLM(),
        inventory=inv,
    )
    assert result.ok is True
    assert out.is_file()
    assert result.warnings == ()
    spec = load_mission_spec(out)
    assert spec.player.airfield == "Manston"
    assert spec.player.aircraft == "SpitfireLFMkIX"
    miz = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "planned.miz")
    assert miz.is_file()


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
    )
    assert result.ok is True
    assert result.spec is not None
    assert result.spec.theatre == "TheChannel"


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
    assert main(["plan", "Manston free flight", "--stub", "-o", str(out)]) == 0
    assert out.is_file()
    assert load_mission_spec(out).player.airfield == "Manston"


def test_cli_plan_live_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    rc = main(["plan", "Manston free flight", "-o", "out/should_not_write.yaml"])
    assert rc == 2
