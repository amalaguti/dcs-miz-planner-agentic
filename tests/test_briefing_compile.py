"""Compile-time briefing dictionary assertions."""

from __future__ import annotations

import zipfile
from pathlib import Path

from fixtures_support import (
    EXAMPLE_SPEC,
    INTERCEPT_SPEC,
    channel_available_inventory,
    compile_intercept,
    compile_manston,
)

from dcs_miz_planner.compiler import PyDCSCompiler
from dcs_miz_planner.loader import load_mission_spec


def _read_dictionary(miz: Path) -> str:
    with zipfile.ZipFile(miz) as z:
        assert "l10n/DEFAULT/dictionary" in z.namelist()
        return z.read("l10n/DEFAULT/dictionary").decode("utf-8")


def test_compile_freeflight_fills_briefing(tmp_path: Path) -> None:
    spec = load_mission_spec(EXAMPLE_SPEC)
    miz = compile_manston(tmp_path / "ff.miz")
    raw = _read_dictionary(miz)
    assert f'["DictKey_Translation_4"]="{spec.name}"' in raw
    assert '["DictKey_Translation_1"]=""' not in raw
    assert '["DictKey_Translation_2"]=""' not in raw
    assert '["DictKey_Translation_3"]=""' in raw  # opposing task empty for blue player
    assert "Cold start at Manston" in raw
    assert "familiarisation" in raw or "Free flight" in raw


def test_compile_intercept_fills_player_task(tmp_path: Path) -> None:
    spec = load_mission_spec(INTERCEPT_SPEC)
    miz = compile_intercept(tmp_path / "ix.miz")
    raw = _read_dictionary(miz)
    assert f'["DictKey_Translation_4"]="{spec.name}"' in raw
    assert '["DictKey_Translation_1"]=""' not in raw
    assert '["DictKey_Translation_2"]=""' not in raw
    assert "intercept" in raw.lower() or "Bf-109" in raw or "climb" in raw.lower()


def test_compile_voice_override_changes_register(tmp_path: Path) -> None:
    spec = load_mission_spec(EXAMPLE_SPEC)
    inv = channel_available_inventory()
    raf = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "raf.miz", voice="raf")
    usaaf = PyDCSCompiler(inventory=inv).compile(spec, tmp_path / "usaaf.miz", voice="usaaf")
    raf_raw = _read_dictionary(raf)
    usaaf_raw = _read_dictionary(usaaf)
    assert f'["DictKey_Translation_4"]="{spec.name}"' in raf_raw
    assert f'["DictKey_Translation_4"]="{spec.name}"' in usaaf_raw
    assert raf_raw != usaaf_raw
    assert "Listen up" in usaaf_raw
    assert "You're away" in raf_raw or "Right." in raf_raw
