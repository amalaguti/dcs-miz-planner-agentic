"""Expand recon find beat into typed zones/triggers (no Lua / no PyDCS)."""

from __future__ import annotations

from .models import (
    CoalitionInZoneCondition,
    MarkAction,
    MessageAction,
    MissionSpec,
    MissionType,
    SetFlagAction,
    TimeMoreCondition,
    TriggerRule,
    TriggerZone,
)

RECON_AOI_ZONE = "recon_aoi"
RECON_FIND_FLAG = "830"
RECON_FIND_MESSAGE = "Area observed — RTB when ready."
RECON_MARK_TEXT = "Recon AOI"


def expand_recon_find_pack(spec: MissionSpec) -> MissionSpec:
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
    return spec.model_copy(update={"zones": [zone], "triggers": triggers})
