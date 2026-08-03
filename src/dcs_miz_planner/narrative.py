"""Opt-in mission narrative packs → typed zones/triggers (no Lua)."""

from __future__ import annotations

from .agent.voice import DEFAULT_VOICE, resolve_voice
from .models import (
    CoalitionInZoneCondition,
    MessageAction,
    MissionEndAction,
    MissionEndResult,
    MissionSpec,
    MissionType,
    NarrativeSpec,
    TimeMoreCondition,
    TriggerRule,
    TriggerZone,
    UnitDeadCondition,
)

CAP_STATION_ZONE = "cap_station"
CAP_STATION_RADIUS_M = 5000.0
CAP_PUSH_SECONDS = 120.0

_CAP_COPY: dict[str, dict[str, str]] = {
    "raf": {
        "push": ("Ops — scramble and establish CAP at the briefed station. Weapons as briefed."),
        "on_station": ("On station. CAP established — expect bandits. Engage per ROE."),
        "win": "Splash — bandits down. Well done. You are cleared to RTB.",
    },
    "usaaf": {
        "push": ("Ops — get airborne and take the CAP station as briefed. Weapons per ROE."),
        "on_station": ("On station. CAP set — watch for bogeys. Engage per ROE."),
        "win": "Bandits down. Good work. Cleared to RTB.",
    },
    "neutral": {
        "push": "Climb and establish CAP at the briefed station.",
        "on_station": "On station. CAP established. Engage per ROE.",
        "win": "Hostiles destroyed. Mission success. Return to base.",
    },
}


class NarrativeError(Exception):
    """Narrative pack cannot be applied; maps to a validation-style error."""

    def __init__(
        self,
        code: str,
        path: str,
        message: str,
        *,
        hint: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message
        self.hint = hint


def expand_narrative_if_needed(
    spec: MissionSpec,
    *,
    voice: str | None = None,
) -> MissionSpec:
    """Return Spec unchanged, or with CAP narrative materialised into zones/triggers."""
    if spec.narrative is None or not spec.narrative.enabled:
        return spec
    return apply_narrative(spec, voice=voice)


def apply_narrative(spec: MissionSpec, *, voice: str | None = None) -> MissionSpec:
    """Expand ``narrative.enabled`` into typed zones/triggers; clear the opt-in flag."""
    if spec.narrative is None or not spec.narrative.enabled:
        return spec

    if spec.zones or spec.triggers:
        raise NarrativeError(
            "narrative_conflict",
            "narrative",
            "narrative.enabled cannot be used when zones or triggers are already set",
            hint="Clear zones/triggers, or set narrative.enabled false and keep hand-written rules",
        )

    if spec.mission_type is not MissionType.CAP:
        raise NarrativeError(
            "narrative_unsupported_mission_type",
            "narrative",
            (
                f"narrative.enabled is only supported for mission_type cap "
                f"(got {spec.mission_type.value!r})"
            ),
            hint="Disable narrative, or use mission_type cap",
        )

    if spec.cap is None:
        raise NarrativeError(
            "narrative_cap_required",
            "cap",
            "CAP narrative requires a nested cap block",
        )

    if not spec.enemies:
        raise NarrativeError(
            "narrative_enemies_required",
            "enemies",
            "CAP narrative requires at least one enemy flight for the win condition",
        )

    resolved = resolve_voice(cli_voice=voice) if voice else DEFAULT_VOICE
    if resolved not in _CAP_COPY:
        resolved = DEFAULT_VOICE
    copy = _CAP_COPY[resolved]

    zone = TriggerZone(
        name=CAP_STATION_ZONE,
        bearing_deg=spec.cap.bearing_deg,
        distance_km=spec.cap.distance_km,
        radius_m=CAP_STATION_RADIUS_M,
    )

    triggers = [
        TriggerRule(
            name="narrative_push",
            once=True,
            when=[TimeMoreCondition(seconds=CAP_PUSH_SECONDS)],
            then=[MessageAction(text=copy["push"], duration_s=12)],
        ),
        TriggerRule(
            name="narrative_on_station",
            once=True,
            when=[
                CoalitionInZoneCondition(
                    zone=CAP_STATION_ZONE,
                    coalition=spec.player.coalition,
                )
            ],
            then=[MessageAction(text=copy["on_station"], duration_s=12)],
        ),
        TriggerRule(
            name="narrative_bandits_down",
            once=True,
            when=[UnitDeadCondition(enemy_index=0)],
            then=[
                MessageAction(text=copy["win"], duration_s=15),
                MissionEndAction(result=MissionEndResult.WIN),
            ],
        ),
    ]

    return spec.model_copy(
        update={
            "zones": [zone],
            "triggers": triggers,
            "narrative": NarrativeSpec(enabled=False),
        }
    )
