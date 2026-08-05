"""Soft immersion floor: cue detection + host repair nudge for vague invent."""

from __future__ import annotations

import re

from ..models import MissionSpec, MissionType

# Prompt cues → (behaviour_id, example path, human reason)
_CUE_RULES: tuple[tuple[re.Pattern[str], str, str, str], ...] = (
    (
        re.compile(
            r"\b(interesting|surprise|immersive|immersion|keeps?\s+me\s+honest|"
            r"honest|discipline|challenge|don'?t\s+over-?specify)\b",
            re.IGNORECASE,
        ),
        "altitude_speed_gates",
        "examples/manston_freeflight_altitude_speed_gates.yaml",
        "vague free_flight / hop immersion",
    ),
    (
        re.compile(
            r"\b(find|mark|smoke|target\s+area|help\s+me\s+find|findability)\b",
            re.IGNORECASE,
        ),
        "mark_smoke",
        "examples/manston_ground_attack_markers.yaml",
        "find / mark the strike area",
    ),
    (
        re.compile(
            r"\b(big\s+show|beware|epsom|campaign|fight\s+or\s+die)\b",
            re.IGNORECASE,
        ),
        "radio_late_activation",
        "examples/manston_dawn_intercept_radio.yaml",
        "campaign-named ask (call list_installed_campaigns, then map to behaviours)",
    ),
    (
        re.compile(
            r"\b(choose\s+difficulty|difficulty\s+menu|i\s+choose|"
            r"f10|radio\s+menu)\b",
            re.IGNORECASE,
        ),
        "radio_late_activation",
        "examples/manston_dawn_intercept_radio.yaml",
        "player-chosen difficulty",
    ),
    (
        re.compile(
            r"\b(don'?t\s+want\s+to\s+write\s+triggers|narrative|"
            r"immersive\s+but)\b",
            re.IGNORECASE,
        ),
        "narrative_pack",
        "examples/manston_cap_narrative.yaml",
        "narrative immersion without hand triggers",
    ),
)


def immersion_cues(prompt: str) -> list[tuple[str, str, str]]:
    """Return list of (behaviour_id, example_path, reason) matched in ``prompt``."""
    text = prompt or ""
    out: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for pattern, behaviour, example, reason in _CUE_RULES:
        if pattern.search(text) and behaviour not in seen:
            seen.add(behaviour)
            out.append((behaviour, example, reason))
    return out


def _has_altitude_or_speed(spec: MissionSpec) -> bool:
    for trig in spec.triggers or []:
        for cond in trig.when or []:
            t = getattr(cond, "type", "")
            if t in {
                "unit_altitude_higher",
                "unit_altitude_lower",
                "unit_speed_higher",
                "unit_speed_lower",
            }:
                return True
    return False


def _has_mark_or_smoke(spec: MissionSpec) -> bool:
    for trig in spec.triggers or []:
        for act in trig.then or []:
            if getattr(act, "type", "") in {"mark", "smoke"}:
                return True
    return False


def _has_radio_activate(spec: MissionSpec) -> bool:
    acts = {getattr(a, "type", "") for trig in (spec.triggers or []) for a in (trig.then or [])}
    return "radio_item_add" in acts and "activate_group" in acts


def _has_narrative(spec: MissionSpec) -> bool:
    return bool(getattr(getattr(spec, "narrative", None), "enabled", False))


def _has_sound_or_flags(spec: MissionSpec) -> bool:
    for trig in spec.triggers or []:
        for act in trig.then or []:
            if getattr(act, "type", "") in {"sound", "inc_flag", "set_flag_value"}:
                return True
        for cond in trig.when or []:
            if getattr(cond, "type", "") in {
                "flag_equals",
                "flag_more",
                "flag_less",
                "time_since_flag",
            }:
                return True
    return False


def spec_satisfies_behaviour(spec: MissionSpec, behaviour_id: str) -> bool:
    """True when Spec already shows the packaged behaviour signals."""
    if behaviour_id == "altitude_speed_gates":
        return _has_altitude_or_speed(spec) or _has_sound_or_flags(spec)
    if behaviour_id == "mark_smoke":
        return _has_mark_or_smoke(spec) or any(
            getattr(c, "type", "") == "group_life_less"
            for trig in (spec.triggers or [])
            for c in (trig.when or [])
        )
    if behaviour_id == "radio_late_activation":
        late = any(getattr(e, "late_activation", False) for e in (spec.enemies or []))
        return late and _has_radio_activate(spec)
    if behaviour_id == "narrative_pack":
        return _has_narrative(spec)
    if behaviour_id == "sound_flag_chain":
        return _has_sound_or_flags(spec)
    return True


def immersion_gap(prompt: str, spec: MissionSpec) -> tuple[str, str, str] | None:
    """First unmatched cue for this Spec, or None if floor is satisfied / no cues."""
    mt = spec.mission_type
    for behaviour, example, reason in immersion_cues(prompt):
        if behaviour == "altitude_speed_gates" and mt is not MissionType.FREE_FLIGHT:
            continue
        if behaviour == "mark_smoke" and mt is not MissionType.GROUND_ATTACK:
            continue
        if behaviour == "radio_late_activation" and mt not in {
            MissionType.INTERCEPT,
            MissionType.CAP,
            MissionType.ESCORT,
        }:
            continue
        if behaviour == "narrative_pack" and mt not in {
            MissionType.CAP,
            MissionType.INTERCEPT,
            MissionType.ESCORT,
            MissionType.GROUND_ATTACK,
        }:
            continue
        if not spec_satisfies_behaviour(spec, behaviour):
            return behaviour, example, reason
    return None


def host_immersion_repair_nudge(prompt: str, spec: MissionSpec) -> str | None:
    """User-role message asking for one immersion repair, or None if OK."""
    gap = immersion_gap(prompt, spec)
    if gap is None:
        return None
    behaviour, example, reason = gap
    return (
        "[Host] Immersion floor: your Spec validates but looks bare for this ask "
        f"({reason}). Apply packaged mission_behaviour {behaviour!r} "
        f"(see {example}), or sound_flag_chain if more appropriate for free_flight. "
        "Call list_mission_options / get_mission_spec_schema if needed. "
        "If the ask named a campaign, call list_installed_campaigns first and map "
        "themes onto behaviours — never import .miz. "
        "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
    )
