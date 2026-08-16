"""Local gitignored research/ QAG HTML as offline research_guidance colour."""

from __future__ import annotations

from pathlib import Path

import pytest

from dcs_miz_planner.agent.prompts import compose_system_prompt
from dcs_miz_planner.tools import research as research_mod
from dcs_miz_planner.tools.qag_fixtures import (
    is_qag_fixture_source,
    load_qag_index,
    qag_fixture_notes,
)
from dcs_miz_planner.tools.surface import research_guidance

_STUB = """\
<html><head><title>{title}</title></head><body>
<h1>{title}</h1>
<p class="lead">Educational QAG reference for tests.</p>
<div class="note warn">QAG class names are generator labels.</div>
<code>FH Pak 40 75mm</code>
</body></html>
"""


def _stub_research(tmp_path: Path) -> Path:
    pages = {p.id: p for p in load_qag_index()}
    for page in pages.values():
        if not page.html:
            continue
        dest = tmp_path / Path(*Path(page.html).parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(_STUB.format(title=page.title), encoding="utf-8")
    return tmp_path


@pytest.fixture
def local_research(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = _stub_research(tmp_path)
    monkeypatch.setattr(
        "dcs_miz_planner.tools.qag_fixtures.resolve_research_root",
        lambda explicit=None: root if explicit is None else Path(explicit),
    )
    return root


def test_qag_index_skips_duplicate_cold_war_anti_ship() -> None:
    pages = {p.id: p for p in load_qag_index()}
    assert pages["wwii-anti-ship"].enabled is True
    assert pages["cw-anti-ship"].enabled is False
    assert "duplicate" in pages["cw-anti-ship"].skip_reason.lower()


def test_offline_ground_attack_returns_qag_fixture(local_research: Path) -> None:
    del local_research
    result = research_guidance(
        "Channel artillery strike on armor and infantry",
        mission_type="ground_attack",
        theatre="TheChannel",
        live=False,
    )
    assert result["ok"] is True
    qag = [n for n in result["notes"] if is_qag_fixture_source(n["source"])]
    assert qag
    assert any("wwii-ground" in n["source"] or "ground" in n["source"] for n in qag)
    blob = " ".join(n["snippet"] for n in qag).lower()
    assert "qag ui names" in blob
    assert "not spec" in blob


def test_offline_mission_design_focus_returns_qag(local_research: Path) -> None:
    del local_research
    result = research_guidance(
        "design a strike",
        focus="mission_design",
        live=False,
    )
    assert result["ok"] is True
    assert any(is_qag_fixture_source(n["source"]) for n in result["notes"])


def test_anti_ship_query_does_not_double_wwii_page(local_research: Path) -> None:
    del local_research
    result = research_guidance(
        "anti-ship submarine LST amphibious",
        mission_type="ground_attack",
        theatre="TheChannel",
        live=False,
    )
    assert result["ok"] is True
    sources = [n["source"] for n in result["notes"] if is_qag_fixture_source(n["source"])]
    assert sources.count("fixture:qag:wwii-anti-ship") == 1
    assert "fixture:qag:cw-anti-ship" not in sources


def test_missing_research_dir_returns_no_qag_notes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "dcs_miz_planner.tools.qag_fixtures.resolve_research_root",
        lambda explicit=None: None,
    )
    notes = qag_fixture_notes(query="artillery strike", mission_type="ground_attack")
    assert notes == []
    result = research_guidance(
        "Channel artillery strike",
        mission_type="ground_attack",
        live=False,
    )
    assert result["ok"] is True
    assert not any(is_qag_fixture_source(n["source"]) for n in result["notes"])


def test_intercept_canned_notes_still_present() -> None:
    result = research_guidance(
        "Channel Spitfire intercept vs Bf-109",
        mission_type="intercept",
        live=False,
    )
    assert result["ok"] is True
    assert any(n["source"] == "fixture:intercept_doctrine" for n in result["notes"])
    assert result["retrieval"] == "fixture"
    assert all(research_mod.is_fixture_source(n["source"]) for n in result["notes"])


def test_prompt_forbids_qag_labels_as_spec_ids() -> None:
    prompt = compose_system_prompt("neutral")
    assert "QAG" in prompt
    assert "SEAD" in prompt
    assert "not Spec or PyDCS ids" in prompt or "not Spec or PyDCS" in prompt
