"""Soft immersion floor: cue detection + host repair nudge for vague invent."""

from __future__ import annotations

import re

from ..models import MissionSpec, MissionType
from ..registry import ChannelRegistry, RegistryError, get_channel_registry

_HARBOUR_CUE = re.compile(
    r"\b(harbour|harbor|dock|alongside|tied\s*up|in\s+port|at\s+port)\b",
    re.IGNORECASE,
)

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
    """User-role message asking for one immersion repair, or None if OK.

    Channel-only: packaged ``mission_behaviour`` examples are Manston YAML.
    Do not cite those paths on other theatres (Falklands/Nevada/Syria/Caucasus Stage A).
    """
    if spec.theatre != "TheChannel":
        return None
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


def harbour_prompt_cues(prompt: str) -> bool:
    """True when the pilot ask mentions harbour/dock shipping."""
    return bool(_HARBOUR_CUE.search(prompt or ""))


_THEATRE_ALLOWED_TYPES: dict[str, frozenset[MissionType]] = {
    "TheChannel": frozenset(MissionType),
    "Normandy": frozenset(MissionType),
    "Caucasus": frozenset(MissionType),
    "Syria": frozenset(MissionType),
    "Nevada": frozenset(MissionType),
    "Falklands": frozenset({MissionType.FREE_FLIGHT, MissionType.CAP}),
}


def host_theatre_mission_refuse_nudge(spec: MissionSpec) -> str | None:
    """Refuse mission types not allowed on this theatre. Every turn.

    TheChannel: all six. Normandy: all six. Caucasus: all six.
    Syria: all six. Nevada: all six. Falklands: free_flight or CAP.
    Else (Stage A): free_flight only. Callers MUST treat a non-None result
    as a hard refuse: never capture a draft and never write YAML. A one-shot
    ``_used`` flag is not.
    """
    allowed = _THEATRE_ALLOWED_TYPES.get(spec.theatre, frozenset({MissionType.FREE_FLIGHT}))
    if spec.mission_type in allowed:
        return None
    if spec.theatre == "Normandy":
        return (
            "[Host] Normandy invent is all six types at NeedsOarPoint. "
            "Emit free_flight, CAP (station 180°/63 km toward Cherbourg, not Manston 135/25), "
            "ground_attack or recon (AOI 180°/133 km inland of Maupertus, not Manston "
            "125/76), intercept or escort on the Cherbourg corridor (not Hawkinge, "
            "not Manston 120/55) "
            "or switch theatre to TheChannel. Do not copy channel_place "
            "geometry (french coast belts, Hawkinge) onto Normandy. "
            "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    if spec.theatre == "Caucasus":
        return (
            "[Host] Caucasus invent is all six types at Batumi. "
            "Emit free_flight, CAP (station 270°/40 km west over the Black Sea, not Manston 135/25), "
            "ground_attack or recon (AOI 43°/110 km inland past Kutaisi, not Manston "
            "125/76, not CAP 270/40), intercept or escort on the Black Sea corridor (not Hawkinge, "
            "not Manston 120/55) "
            "or switch theatre to TheChannel. Do not copy channel_place or NeedsOarPoint "
            "geometry onto Caucasus. "
            "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    if spec.theatre == "Syria":
        return (
            "[Host] Syria invent is all six types at Incirlik. "
            "Emit free_flight, CAP, intercept, or escort (station 180°/40 km south over "
            "the Gulf of Iskenderun — not Cherbourg 180/63, not Batumi 270/40, not "
            "Hawkinge, not escort 120/55) or ground_attack or recon (AOI 121°/200 km inland "
            "past Aleppo — not CAP 180/40, not Manston 125/76, not Kutaisi 43/110) "
            "or switch theatre to "
            "TheChannel. Do not copy channel_place or NeedsOarPoint geometry onto Syria. "
            "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    if spec.theatre == "Nevada":
        return (
            "[Host] Nevada invent is all six types at Nellis. "
            "Emit free_flight, CAP, intercept, or escort "
            "(station 350°/40 km desert north-range, not Incirlik 180/40, "
            "not Batumi 270/40, not Channel escort 120/55) or ground_attack or recon "
            "(303°/85 km inland past Creech, not CAP 350/40) or switch theatre to TheChannel. "
            "Do not copy channel_place or NeedsOarPoint geometry onto Nevada. "
            "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    if spec.theatre == "Falklands":
        return (
            "[Host] Falklands invent is free_flight or CAP at Mount Pleasant. "
            "Refuse intercept/ground_attack/escort/recon — emit free_flight or CAP "
            "(Su-25T, UK blue, sunny_clear; CAP station 150°/40 km South Atlantic) "
            "or switch theatre to TheChannel. "
            "Do not copy channel_place or NeedsOarPoint geometry onto Falklands. "
            "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
        )
    return (
        f"[Host] {spec.theatre} invent is free_flight only. "
        "Refuse intercept/cap/ground_attack/escort/recon — emit free_flight "
        "or switch theatre to TheChannel. "
        "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
    )


def host_normandy_combat_nudge(spec: MissionSpec) -> str | None:
    """Alias for :func:`host_theatre_mission_refuse_nudge` (existing tests import this)."""
    return host_theatre_mission_refuse_nudge(spec)


def theatre_mission_refuse_chat_line(spec: MissionSpec) -> str:
    """User-facing chat refuse after a combat JSON (draft not captured)."""
    if spec.theatre == "Normandy":
        return (
            "[Host] Normandy unexpected mission type is not inventable — "
            "commander nudged toward NeedsOarPoint (all six types) or TheChannel. "
            "Draft NOT captured. Emit a Normandy-supported type at NeedsOarPoint "
            "or switch theatre to TheChannel, then /accept."
        )
    if spec.theatre == "Caucasus":
        return (
            "[Host] Caucasus unexpected mission type is not inventable — "
            "commander nudged toward Batumi (all six types) or TheChannel. "
            "Draft NOT captured. Emit a Caucasus-supported type at Batumi "
            "or switch theatre to TheChannel, then /accept."
        )
    if spec.theatre == "Syria":
        return (
            "[Host] Syria unexpected mission type is not inventable — "
            "commander nudged toward Incirlik (all six types) or TheChannel. "
            "Draft NOT captured. Emit a Syria-supported type at Incirlik "
            "or switch theatre to TheChannel, then /accept."
        )
    if spec.theatre == "Nevada":
        return (
            "[Host] Nevada unexpected mission type is not inventable — "
            "commander nudged toward Nellis (all six types) or TheChannel. "
            "Draft NOT captured. Emit a Nevada-supported type at Nellis "
            "or switch theatre to TheChannel, then /accept."
        )
    if spec.theatre == "Falklands":
        return (
            "[Host] Falklands intercept/GA/escort/recon is not inventable — "
            "commander nudged toward Mount Pleasant free_flight or CAP, or TheChannel. "
            "Draft NOT captured. Emit free_flight or CAP at Mount Pleasant or switch "
            "theatre to TheChannel, then /accept."
        )
    return (
        f"[Host] {spec.theatre} combat is not inventable — "
        "commander nudged toward free_flight or TheChannel. "
        "Draft NOT captured. Emit free_flight or switch theatre to TheChannel, then /accept."
    )


def theatre_mission_refuse_accept_line(spec: MissionSpec) -> str:
    """User-facing /accept refuse (draft not written)."""
    if spec.theatre == "Normandy":
        return (
            "Normandy unexpected mission type is not inventable. Draft NOT written. "
            "Emit a Normandy-supported type at NeedsOarPoint "
            "or switch theatre to TheChannel."
        )
    if spec.theatre == "Caucasus":
        return (
            "Caucasus unexpected mission type is not inventable. Draft NOT written. "
            "Emit a Caucasus-supported type at Batumi "
            "or switch theatre to TheChannel."
        )
    if spec.theatre == "Syria":
        return (
            "Syria unexpected mission type is not inventable. Draft NOT written. "
            "Emit a Syria-supported type at Incirlik "
            "or switch theatre to TheChannel."
        )
    if spec.theatre == "Nevada":
        return (
            "Nevada unexpected mission type is not inventable. Draft NOT written. "
            "Emit a Nevada-supported type at Nellis "
            "or switch theatre to TheChannel."
        )
    if spec.theatre == "Falklands":
        return (
            "Falklands intercept/GA/escort/recon is not inventable. Draft NOT written. "
            "Emit free_flight or CAP at Mount Pleasant or switch theatre to TheChannel."
        )
    return (
        f"{spec.theatre} combat is not inventable. Draft NOT written. "
        "Emit free_flight or switch theatre to TheChannel."
    )


def theatre_mission_refuse_planner_error(spec: MissionSpec) -> str:
    """Planner last_parse_error when combat is refused on this theatre."""
    if spec.theatre == "Normandy":
        return "Normandy invent is all six types at NeedsOarPoint"
    if spec.theatre == "Caucasus":
        return "Caucasus invent is all six types at Batumi"
    if spec.theatre == "Syria":
        return "Syria invent is all six types at Incirlik"
    if spec.theatre == "Nevada":
        return "Nevada invent is all six types at Nellis"
    if spec.theatre == "Falklands":
        return "Falklands invent is free_flight or CAP; intercept/GA/escort/recon are refused"
    return f"{spec.theatre} invent is free_flight only; combat types are refused"


def host_harbour_unit_nudge(
    prompt: str,
    spec: MissionSpec,
    *,
    registry: ChannelRegistry | None = None,
) -> str | None:
    """Nudge when harbour cues conflict with land-domain targets (no unit auto-swap)."""
    if spec.theatre != "TheChannel":
        return None
    if not harbour_prompt_cues(prompt):
        return None
    if spec.mission_type not in {MissionType.GROUND_ATTACK, MissionType.RECON}:
        return None
    if not spec.targets:
        return None
    reg = registry or get_channel_registry()
    land_ids: list[str] = []
    for tgt in spec.targets:
        try:
            unit = reg.get_strike_unit(tgt.unit)
        except RegistryError:
            continue
        if unit.domain == "land":
            land_ids.append(tgt.unit)
    if not land_ids:
        return None
    shown = ", ".join(land_ids[:4])
    return (
        "[Host] Harbour/dock invent: your Spec uses land units "
        f"({shown}) but harbour asks need sea_craft only. Call "
        "list_strike_targets(domain=sea), use channel_place coastal_harbour "
        "(~120° / 68 km coastal water), motion static, ai_preset harbour_static "
        "(e.g. Uboat_VIIC or Dry-cargo — never Blitz/Bedford trucks). "
        "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."
    )
