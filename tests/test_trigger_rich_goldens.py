"""Structural golden regression for trigger-rich Manston example Specs."""

from __future__ import annotations

from pathlib import Path

from fixtures_support import (
    GATES_FIXTURE_DIR,
    MARKERS_FIXTURE_DIR,
    RADIO_FIXTURE_DIR,
    SOUND_FLAGS_FIXTURE_DIR,
    assert_matches_golden,
    compile_gates,
    compile_markers,
    compile_radio,
    compile_sound_flags,
)


def test_radio_golden_fixtures_exist():
    assert (RADIO_FIXTURE_DIR / "meta.json").is_file()
    assert (RADIO_FIXTURE_DIR / "theatre").is_file()
    assert (RADIO_FIXTURE_DIR / "mission").is_file()


def test_radio_compile_matches_golden(tmp_path: Path):
    out = compile_radio(tmp_path / "radio.miz")
    assert_matches_golden(out, RADIO_FIXTURE_DIR)


def test_gates_golden_fixtures_exist():
    assert (GATES_FIXTURE_DIR / "meta.json").is_file()
    assert (GATES_FIXTURE_DIR / "theatre").is_file()
    assert (GATES_FIXTURE_DIR / "mission").is_file()


def test_gates_compile_matches_golden(tmp_path: Path):
    out = compile_gates(tmp_path / "gates.miz")
    assert_matches_golden(out, GATES_FIXTURE_DIR)


def test_markers_golden_fixtures_exist():
    assert (MARKERS_FIXTURE_DIR / "meta.json").is_file()
    assert (MARKERS_FIXTURE_DIR / "theatre").is_file()
    assert (MARKERS_FIXTURE_DIR / "mission").is_file()


def test_markers_compile_matches_golden(tmp_path: Path):
    out = compile_markers(tmp_path / "markers.miz")
    assert_matches_golden(out, MARKERS_FIXTURE_DIR)


def test_sound_flags_golden_fixtures_exist():
    assert (SOUND_FLAGS_FIXTURE_DIR / "meta.json").is_file()
    assert (SOUND_FLAGS_FIXTURE_DIR / "theatre").is_file()
    assert (SOUND_FLAGS_FIXTURE_DIR / "mission").is_file()


def test_sound_flags_compile_matches_golden(tmp_path: Path):
    out = compile_sound_flags(tmp_path / "sound_flags.miz")
    assert_matches_golden(out, SOUND_FLAGS_FIXTURE_DIR)
