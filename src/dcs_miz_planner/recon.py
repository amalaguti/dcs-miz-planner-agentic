"""Expand recon find beat into typed zones/triggers (no Lua / no PyDCS)."""

from __future__ import annotations

from .models import (
    CoalitionInZoneCondition,
    MarkAction,
    MessageAction,
    MissionSpec,
    MissionType,
    NarrativeSpec,
    SetFlagAction,
    TimeMoreCondition,
    TriggerRule,
    TriggerZone,
)

RECON_AOI_ZONE = "recon_aoi"
RECON_FIND_FLAG = "830"
RECON_FIND_MESSAGE = "Area observed — RTB when ready."
RECON_MARK_TEXT = "Recon AOI"
RECON_PUSH_SECONDS = 120.0

_RECON_PUSH: dict[str, str] = {
    "raf": (
        "Ops — climb for the Channel recce. Observe the briefed area, weapons hold, "
        "and report what you see."
    ),
    "usaaf": (
        "Ops — climb for the recce. Observe the briefed area, weapons hold, "
        "and report what you see."
    ),
    "neutral": "Climb to the briefed recon area. Observe contacts. Weapons hold.",
}


def expand_recon_find_pack(spec: MissionSpec, *, voice: str | None = None) -> MissionSpec:
    """Inject AOI zone + mark/find triggers for recon after validation."""
    if spec.mission_type is not MissionType.RECON:
        return spec
    if spec.recon is None:
        raise ValueError("recon: recon missions require a nested recon block")
    if spec.zones or spec.triggers:
        raise ValueError(
            "zones/triggers: recon v1 requires empty zones/triggers "
            "(compiler injects the AOI find beat)"
        )

    recon = spec.recon
    zone = TriggerZone(
        name=RECON_AOI_ZONE,
        bearing_deg=recon.bearing_deg,
        distance_km=recon.distance_km,
        radius_m=recon.radius_m,
    )
    triggers: list[TriggerRule] = []
    narrative_on = spec.narrative is not None and spec.narrative.enabled
    if narrative_on:
        from .agent.voice import DEFAULT_VOICE, resolve_voice

        resolved = resolve_voice(cli_voice=voice) if voice else DEFAULT_VOICE
        push = _RECON_PUSH.get(resolved, _RECON_PUSH[DEFAULT_VOICE])
        triggers.append(
            TriggerRule(
                name="narrative_push",
                once=True,
                when=[TimeMoreCondition(seconds=RECON_PUSH_SECONDS)],
                then=[MessageAction(text=push, duration_s=12)],
            )
        )
    if recon.mark:
        triggers.append(
            TriggerRule(
                name="recon_aoi_mark",
                once=True,
                when=[TimeMoreCondition(seconds=1)],
                then=[MarkAction(zone=RECON_AOI_ZONE, text=RECON_MARK_TEXT, readonly=True)],
            )
        )
    triggers.append(
        TriggerRule(
            name="recon_area_observed",
            once=True,
            when=[
                CoalitionInZoneCondition(
                    zone=RECON_AOI_ZONE,
                    coalition=spec.player.coalition,
                )
            ],
            then=[
                MessageAction(text=RECON_FIND_MESSAGE, duration_s=12),
                SetFlagAction(flag=RECON_FIND_FLAG, value=True),
            ],
        )
    )
    update: dict[str, object] = {"zones": [zone], "triggers": triggers}
    if narrative_on:
        update["narrative"] = NarrativeSpec(enabled=False)
    return spec.model_copy(update=update)
