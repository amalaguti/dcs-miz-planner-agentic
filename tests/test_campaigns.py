"""Hermetic tests for Mods/campaigns index (no real DCS root required)."""

from __future__ import annotations

from pathlib import Path

import pytest

from dcs_miz_planner.install.campaigns import index_installed_campaigns, scan_campaigns_root
from dcs_miz_planner.install.doc_extract import DocTextCache, excerpt_for_pdf
from dcs_miz_planner.tools import list_installed_campaigns


def _write_fixture_campaign(campaigns: Path) -> Path:
    pack = campaigns / "Spitfire Fixture Campaign"
    pack.mkdir(parents=True)
    (pack / "Fixture.cmp").write_text(
        """campaign =
{
    ["name_EN"] = "Spitfire Fixture Campaign",
    ["description"] = "A short fixture description for tests.",
    ["stages"] =
    {
        [1] =
        {
            ["name"] = "Stage 1",
            ["missions"] =
            {
                [1] =
                {
                    ["file"] = "Fixture - 01.miz",
                    ["description"] = "",
                },
            },
        },
        [2] =
        {
            ["name"] = "Stage 2",
            ["missions"] =
            {
                [1] =
                {
                    ["file"] = "Fixture - 02.miz",
                    ["description"] = "",
                },
            },
        },
    },
}
""",
        encoding="utf-8",
    )
    (pack / "Fixture - 01.miz").write_bytes(b"PK\x03\x04fake")
    (pack / "Fixture - 02.miz").write_bytes(b"PK\x03\x04fake")
    doc = pack / "Doc"
    doc.mkdir()
    # Bytes need only exist on disk for size/mtime cache identity; extract is mocked.
    (doc / "Fixture - Mission 01.pdf").write_bytes(b"%PDF-1.4 fixture body")
    (doc / "Fixture - Campaign introduction.pdf").write_bytes(b"%PDF-1.4 intro body")
    return pack


def test_scan_campaigns_lists_cmp_miz_and_docs(tmp_path: Path) -> None:
    campaigns = tmp_path / "campaigns"
    campaigns.mkdir()
    _write_fixture_campaign(campaigns)

    summaries = scan_campaigns_root(campaigns)
    assert len(summaries) == 1
    s = summaries[0]
    assert s.name == "Spitfire Fixture Campaign"
    assert s.description and "fixture description" in s.description.lower()
    assert [m.filename for m in s.missions] == ["Fixture - 01.miz", "Fixture - 02.miz"]
    assert {d.filename for d in s.docs} == {
        "Fixture - Mission 01.pdf",
        "Fixture - Campaign introduction.pdf",
    }
    assert s.cmp_file == "Fixture.cmp"


def test_index_via_campaigns_dir_override(tmp_path: Path) -> None:
    campaigns = tmp_path / "campaigns"
    campaigns.mkdir()
    _write_fixture_campaign(campaigns)

    index = index_installed_campaigns(campaigns_dir=campaigns)
    assert len(index.campaigns) == 1
    assert index.campaigns[0].missions[0].filename.endswith(".miz")


def test_list_installed_campaigns_tool_fixture(tmp_path: Path) -> None:
    campaigns = tmp_path / "campaigns"
    campaigns.mkdir()
    _write_fixture_campaign(campaigns)

    result = list_installed_campaigns(campaigns_dir=campaigns)
    assert result["ok"] is True
    assert len(result["campaigns"]) == 1
    camp = result["campaigns"][0]
    assert camp["name"] == "Spitfire Fixture Campaign"
    assert "Fixture - 01.miz" in camp["missions"]
    names = [d["filename"] for d in camp["docs"]]
    assert "Fixture - Mission 01.pdf" in names
    assert all(d.get("excerpt") is None for d in camp["docs"])


def test_list_installed_campaigns_missing_install_nonfatal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from dcs_miz_planner.install import campaigns as camp_mod

    def no_roots(**_kwargs):  # type: ignore[no-untyped-def]
        return [], []

    monkeypatch.setattr(camp_mod, "discover_dcs_roots", no_roots)
    result = list_installed_campaigns()
    assert result["ok"] is True
    assert result["campaigns"] == []
    assert "warning" in result


def test_include_doc_text_returns_excerpt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from dcs_miz_planner.install import doc_extract as de

    campaigns = tmp_path / "campaigns"
    campaigns.mkdir()
    _write_fixture_campaign(campaigns)
    db = tmp_path / "cache.sqlite"
    monkeypatch.setattr(
        de, "extract_pdf_text", lambda _p, **_k: "Dawn Channel patrol briefing theme"
    )

    result = list_installed_campaigns(campaigns_dir=campaigns, db_path=db, include_doc_text=True)
    assert result["ok"] is True
    assert result["include_doc_text"] is True
    docs = result["campaigns"][0]["docs"]
    excerpts = [d.get("excerpt") or "" for d in docs]
    assert any("Channel patrol" in e for e in excerpts)


def test_doc_extract_cache_avoids_reread(tmp_path: Path) -> None:
    campaigns = tmp_path / "campaigns"
    campaigns.mkdir()
    pack = _write_fixture_campaign(campaigns)
    pdf = pack / "Doc" / "Fixture - Mission 01.pdf"
    cache = DocTextCache(tmp_path / "cache.sqlite")

    calls = {"n": 0}

    def counting(_path: Path, **_kwargs: object) -> str:
        calls["n"] += 1
        return "cached briefing colour"

    e1, cached1 = excerpt_for_pdf(pdf, cache=cache, extract_fn=counting)
    e2, cached2 = excerpt_for_pdf(pdf, cache=cache, extract_fn=counting)
    assert e1 == "cached briefing colour"
    assert e2 == e1
    assert cached1 is False
    assert cached2 is True
    assert calls["n"] == 1
