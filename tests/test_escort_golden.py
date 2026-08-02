"""Golden-fixture regression for Manston escort."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import ESCORT_FIXTURE_DIR, assert_matches_golden, compile_escort


def test_escort_golden_fixtures_exist():
    assert (ESCORT_FIXTURE_DIR / "meta.json").is_file()
    assert (ESCORT_FIXTURE_DIR / "mission").is_file()
    assert (ESCORT_FIXTURE_DIR / "theatre").is_file()


def test_escort_compile_matches_golden(tmp_path: Path):
    miz = compile_escort(tmp_path / "escort.miz")
    assert_matches_golden(miz, ESCORT_FIXTURE_DIR)
