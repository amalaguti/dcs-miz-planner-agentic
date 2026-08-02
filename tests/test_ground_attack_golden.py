"""Golden-fixture regression for Manston ground-attack."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import GA_FIXTURE_DIR, assert_matches_golden, compile_ground_attack


def test_ground_attack_golden_fixtures_exist():
    assert (GA_FIXTURE_DIR / "meta.json").is_file()
    assert (GA_FIXTURE_DIR / "mission").is_file()
    assert (GA_FIXTURE_DIR / "theatre").is_file()


def test_ground_attack_compile_matches_golden(tmp_path: Path):
    miz = compile_ground_attack(tmp_path / "ga.miz")
    assert_matches_golden(miz, GA_FIXTURE_DIR)
