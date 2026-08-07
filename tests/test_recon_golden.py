"""Golden-fixture regression for Manston recon."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import RECON_FIXTURE_DIR, assert_matches_golden, compile_recon


def test_recon_golden_fixtures_exist():
    assert (RECON_FIXTURE_DIR / "meta.json").is_file()
    assert (RECON_FIXTURE_DIR / "mission").is_file()
    assert (RECON_FIXTURE_DIR / "theatre").is_file()


def test_recon_compile_matches_golden(tmp_path: Path):
    miz = compile_recon(tmp_path / "recon.miz")
    assert_matches_golden(miz, RECON_FIXTURE_DIR)
