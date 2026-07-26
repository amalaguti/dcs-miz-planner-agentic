"""Golden structural regression for Manston cold free-flight compile."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest
from fixtures_support import FIXTURE_DIR, assert_matches_golden, compile_manston


def test_manston_golden_fixtures_exist():
    assert (FIXTURE_DIR / "meta.json").is_file()
    assert (FIXTURE_DIR / "theatre").is_file()
    assert (FIXTURE_DIR / "mission").is_file()


def test_manston_compile_matches_golden(tmp_path: Path):
    out = compile_manston(tmp_path / "manston.miz")
    assert_matches_golden(out)


def test_golden_detects_theatre_mismatch(tmp_path: Path):
    out = compile_manston(tmp_path / "manston.miz")
    bad = tmp_path / "bad.miz"
    with zipfile.ZipFile(out) as src, zipfile.ZipFile(bad, "w") as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "theatre":
                data = b"NotTheChannel"
            dst.writestr(info, data)

    with pytest.raises(AssertionError, match="theatre"):
        assert_matches_golden(bad)
