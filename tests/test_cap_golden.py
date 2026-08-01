"""Golden structural regression for Manston CAP compile."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import (
    CAP_FIXTURE_DIR,
    assert_matches_golden,
    compile_cap,
)


def test_cap_golden_fixtures_exist():
    assert (CAP_FIXTURE_DIR / "meta.json").is_file()
    assert (CAP_FIXTURE_DIR / "theatre").is_file()
    assert (CAP_FIXTURE_DIR / "mission").is_file()


def test_cap_compile_matches_golden(tmp_path: Path):
    out = compile_cap(tmp_path / "cap.miz")
    assert_matches_golden(out, CAP_FIXTURE_DIR)
