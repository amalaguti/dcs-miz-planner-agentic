"""Combined one-shot invent nudges: Spitfire player, WWII colour, dynamics, motion."""

from __future__ import annotations

import re

from ..models import DynamicsMode, MissionSpec, MissionType, TargetMotion

_FROGFOOT_CUE = re.compile(r"\b(su-?25t|frogfoot|su25t)\b", re.IGNORECASE)
_MUSTANG_CUE = re.compile(r"\b(mustang|p-?51)\b", re.IGNORECASE)
_WWII_COLOUR = re.compile(
    r"\b(194[0-5]|ww2|wwii|luftwaffe|bf-?109|fw-?190|third\s*reich|channel\s+war)\b",
    re.IGNORECASE,
)
_DYNAMICS_CHOOSE = re.compile(
    r"\b(f10|f-10|i choose|let me (pick|choose)|choose difficulty|menu)\b",
    re.IGNORECASE,
)
_DYNAMICS_LIVE = re.compile(
    r"\b(unpredictable|dice|different each (time|load)|random (raid|opposition)|"
    r"surprise (me|opposition)|branching|not the same twice)\b",
    re.IGNORECASE,
)
_MOTION_CUE = re.compile(
    r"\b(moving convoy|under way|underway|on the move|patrol(ling)?|"
    r"ships moving|convoy moving)\b",
    re.IGNORECASE,
)

_MODERN_THEATRES = frozenset({"Caucasus", "Syria", "Nevada", "Falklands", "Kola"})
_JSON_ONLY = "Reply with a corrected Mission Spec JSON object ONLY (no markdown fences)."


def host_spitfire_player_nudge(prompt: str, spec: MissionSpec) -> str | None:
    """Nudge Su-25T player → Spitfire unless the ask names Frogfoot/Mustang."""
    text = prompt or ""
    if _FROGFOOT_CUE.search(text) or _MUSTANG_CUE.search(text):
        return None
    if spec.player.aircraft != "Su-25T":
        return None
    return (
        "[Host] Spitfire player: this cockpit is SpitfireLFMkIX. Set "
        "player.aircraft to SpitfireLFMkIX (keep the theatre airfield and "
        "blue country). Leave Su-25T for red AI or escort package unless the "
        "user named Frogfoot. " + _JSON_ONLY
    )


def host_wwii_opposition_nudge(prompt: str, spec: MissionSpec) -> str | None:
    """WWII colour on a modern map should not default red Su-25T enemies."""
    text = prompt or ""
    if spec.theatre not in _MODERN_THEATRES or spec.theatre == "Kola":
        return None
    if not _WWII_COLOUR.search(text):
        return None
    enemies = spec.enemies or []
    if not enemies:
        return None
    if all(e.aircraft != "Su-25T" for e in enemies):
        return None
    return (
        "[Host] WWII colour: enemies should be Bf-109K-4 or FW-190A8 with "
        "country ThirdReich (not Su-25T Russia). Keep player SpitfireLFMkIX "
        "and this theatre's station geometry. " + _JSON_ONLY
    )


def _narrative_on(spec: MissionSpec) -> bool:
    return bool(spec.narrative and spec.narrative.enabled)


def _targets_need_motion(spec: MissionSpec) -> bool:
    if spec.mission_type not in {MissionType.GROUND_ATTACK, MissionType.RECON}:
        return False
    targets = spec.targets or []
    if not targets:
        return False
    return all(t.motion is None or t.motion is TargetMotion.STATIC for t in targets)


def host_dynamics_nudge(prompt: str, spec: MissionSpec) -> str | None:
    """Play-time dynamics and/or moving targets when the ask implies them."""
    text = prompt or ""
    if _narrative_on(spec):
        return None
    has_choose = bool(_DYNAMICS_CHOOSE.search(text))
    has_live = bool(_DYNAMICS_LIVE.search(text))
    want_motion = bool(_MOTION_CUE.search(text)) and _targets_need_motion(spec)

    dyn = spec.dynamics
    dyn_missing = dyn is None or dyn.mode is DynamicsMode.FIXED
    if has_choose and has_live and dyn_missing:
        mode = "hybrid"
    elif has_choose and dyn_missing:
        mode = "choose"
    elif has_live and dyn_missing:
        mode = "live"
    else:
        mode = None

    if mode is None and not want_motion:
        return None

    parts: list[str] = ["[Host] Dynamics / motion:"]
    if mode == "hybrid":
        parts.append(
            "This ask wants both dice and F10 choice. Emit dynamics.mode hybrid "
            "with exclusive pools. See examples/manston_dawn_intercept_dynamics_hybrid.yaml. "
            "Do not enable narrative with dynamics."
        )
    elif mode == "choose":
        parts.append(
            "This ask wants F10 choice. Emit dynamics.mode choose with exclusive "
            "pools (late_activation enemies/targets + menu_label + indices). "
            "See examples/manston_dawn_intercept_dynamics_hybrid.yaml (choose path). "
            "Do not enable narrative with dynamics."
        )
    elif mode == "live":
        parts.append(
            "This ask wants a different turnout each load. Emit dynamics.mode live "
            "with exclusive pools and late_activation enemies (roll min/max). "
            "See examples/manston_dawn_intercept_dynamics_live.yaml. "
            "Do not enable narrative with dynamics."
        )
    if want_motion:
        parts.append(
            "Moving pieces: set targets[].motion to patrol (radius) or path "
            "(2–4 airfield-relative points). Convoys: convoy_transit; ships: "
            "ship_under_way. Do not leave moving asks as static trucks."
        )
    parts.append(_JSON_ONLY)
    return " ".join(parts)


def host_invent_product_nudge(prompt: str, spec: MissionSpec) -> str | None:
    """Join player, WWII opposition, dynamics, and motion repairs into one shot."""
    chunks = [
        host_spitfire_player_nudge(prompt, spec),
        host_wwii_opposition_nudge(prompt, spec),
        host_dynamics_nudge(prompt, spec),
    ]
    present = [c for c in chunks if c]
    if not present:
        return None
    return "\n\n".join(present)
