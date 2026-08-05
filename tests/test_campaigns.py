"""Hermetic tests for Mods/campaigns index (no real DCS root required)."""

from __future__ import annotations

from pathlib import Path

import pytest

from dcs_miz_planner.install.campaigns import index_installed_campaigns, scan_campaigns_root
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
    (doc / "Fixture - Mission 01.pdf").write_bytes(b"%PDF-1.4 fixture")
    (doc / "Fixture - Campaign introduction.pdf").write_bytes(b"%PDF-1.4 intro")
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
    assert "Fixture - Mission 01.pdf" in camp["docs"]


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
