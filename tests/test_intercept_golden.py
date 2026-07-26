"""Golden structural regression for Manston dawn intercept compile."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import (
    INTERCEPT_FIXTURE_DIR,
    assert_matches_golden,
    compile_intercept,
)


def test_intercept_golden_fixtures_exist():
    assert (INTERCEPT_FIXTURE_DIR / "meta.json").is_file()
    assert (INTERCEPT_FIXTURE_DIR / "theatre").is_file()
    assert (INTERCEPT_FIXTURE_DIR / "mission").is_file()


def test_intercept_compile_matches_golden(tmp_path: Path):
    out = compile_intercept(tmp_path / "intercept.miz")
    assert_matches_golden(out, INTERCEPT_FIXTURE_DIR)
