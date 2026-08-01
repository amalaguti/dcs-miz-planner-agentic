"""Squadron voice packs, resolution, and prompt composition."""

from __future__ import annotations

from dcs_miz_planner.agent.prompts import compose_system_prompt
from dcs_miz_planner.agent.voice import (
    DEFAULT_VOICE,
    VOICE_NEUTRAL,
    VOICE_RAF,
    VOICE_USAAF,
    normalize_voice,
    resolve_voice,
)


def test_normalize_aliases() -> None:
    assert normalize_voice("RAF") == VOICE_RAF
    assert normalize_voice("usa") == VOICE_USAAF
    assert normalize_voice("off") == VOICE_NEUTRAL
    assert normalize_voice("nope") is None


def test_resolve_cli_beats_pref() -> None:
    assert resolve_voice(cli_voice="raf", prefs={"squadron_voice": "usaaf"}) == VOICE_RAF


def test_resolve_pref_when_no_cli() -> None:
    assert resolve_voice(prefs={"squadron_voice": "usaaf"}) == VOICE_USAAF


def test_resolve_unknown_falls_back_to_default() -> None:
    assert resolve_voice(cli_voice="not-a-voice") == DEFAULT_VOICE
    assert resolve_voice(prefs={"squadron_voice": "???"}) == DEFAULT_VOICE


def test_compose_raf_includes_persona_and_ops() -> None:
    prompt = compose_system_prompt("raf")
    assert "RAF squadron commander" in prompt
    assert "TheChannel" in prompt
    assert "Tactics" in prompt or "tactics" in prompt
    assert "Watch-outs" in prompt or "watch-outs" in prompt
    assert "Mission Spec JSON" in prompt


def test_compose_usaaf_markers() -> None:
    prompt = compose_system_prompt("usaaf")
    assert "USAAF" in prompt
    assert "RAF Fighter Command" not in prompt


def test_compose_neutral_omits_commander_persona() -> None:
    prompt = compose_system_prompt("neutral")
    assert "RAF squadron commander" not in prompt
    assert "USAAF squadron commander" not in prompt
    assert "TheChannel" in prompt
    assert "research_guidance" in prompt
    assert "cap" in prompt


def test_cap_brief_sections() -> None:
    from pathlib import Path

    from dcs_miz_planner.agent.voice import build_commander_brief
    from dcs_miz_planner.loader import load_mission_spec

    spec = load_mission_spec(Path(__file__).resolve().parents[1] / "examples" / "manston_cap.yaml")
    brief = build_commander_brief(spec, VOICE_RAF)
    assert "## Tactics" in brief
    assert "CAP" in brief or "orbit" in brief.lower()
    assert "weapons_free" in brief or "ROE" in brief
