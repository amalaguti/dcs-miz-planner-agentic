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
    TargetDeadCondition,
    TimeMoreCondition,
    TriggerRule,
    TriggerZone,
    UnitDeadCondition,
)

CAP_STATION_ZONE = "cap_station"
CAP_STATION_RADIUS_M = 5000.0
CAP_PUSH_SECONDS = 120.0
INTERCEPT_SCRAMBLE_SECONDS = 120.0

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

_INTERCEPT_COPY: dict[str, dict[str, str]] = {
    "raf": {
        "scramble": (
            "Ops — scramble. Bandits inbound on the Dover approaches. "
            "Climb and intercept. Weapons free."
        ),
        "win": "Splash — bandits destroyed. Well done. You are cleared to RTB.",
    },
    "usaaf": {
        "scramble": (
            "Ops — scramble. Bogeys inbound toward the Channel approaches. "
            "Climb and intercept. Weapons free."
        ),
        "win": "Bandits down. Good work. Cleared to RTB.",
    },
    "neutral": {
        "scramble": "Scramble. Hostile aircraft inbound. Climb and intercept.",
        "win": "Hostiles destroyed. Mission success. Return to base.",
    },
}

ESCORT_DEST_ZONE = "escort_destination"
ESCORT_DEST_RADIUS_M = 5000.0
ESCORT_PUSH_SECONDS = 120.0

_ESCORT_COPY: dict[str, dict[str, str]] = {
    "raf": {
        "push": (
            "Ops — join the package and escort to the briefed destination. "
            "Watch for bounce. Weapons as briefed."
        ),
        "with_package": (
            "With the package at the destination. Stay sharp — bounce may still be about."
        ),
        "win": "Bounce destroyed. Package covered. Well done. You are cleared to RTB.",
    },
    "usaaf": {
        "push": (
            "Ops — join the package and escort to the briefed destination. "
            "Watch for a bounce. Weapons per ROE."
        ),
        "with_package": ("With the package at destination. Keep eyes out for bogeys."),
        "win": "Bounce down. Package covered. Good work. Cleared to RTB.",
    },
    "neutral": {
        "push": "Join the package and escort to the briefed destination.",
        "with_package": "At the package destination. Remain alert.",
        "win": "Hostiles destroyed. Escort success. Return to base.",
    },
}

STRIKE_AREA_ZONE = "strike_area"
STRIKE_AREA_RADIUS_M = 5000.0
GA_PUSH_SECONDS = 120.0

_GA_COPY: dict[str, dict[str, str]] = {
    "raf": {
        "push": (
            "Ops — climb for the Channel strike. Jettison the tank before the attack run. "
            "Bombs on the briefed targets."
        ),
        "ingress": ("Ingress — strike area. Put your bombs on the targets. Watch for flak."),
        "win": "Targets destroyed. Well done. You are cleared to RTB.",
    },
    "usaaf": {
        "push": (
            "Ops — climb for the strike. Drop the tank before the run. "
            "Bombs on the briefed targets."
        ),
        "ingress": ("Ingress — target area. Put bombs on target. Watch for flak."),
        "win": "Targets down. Good work. Cleared to RTB.",
    },
    "neutral": {
        "push": "Climb to the briefed strike area. Attack the assigned ground targets.",
        "ingress": "At the strike area. Engage the targets.",
        "win": "Targets destroyed. Mission success. Return to base.",
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
    """Return Spec unchanged, or with narrative materialised into zones/triggers."""
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

    resolved = _resolved_voice(voice)

    if spec.mission_type is MissionType.CAP:
        zones, triggers = _apply_cap_pack(spec, resolved)
    elif spec.mission_type is MissionType.INTERCEPT:
        zones, triggers = _apply_intercept_pack(spec, resolved)
    elif spec.mission_type is MissionType.ESCORT:
        zones, triggers = _apply_escort_pack(spec, resolved)
    elif spec.mission_type is MissionType.GROUND_ATTACK:
        zones, triggers = _apply_ground_attack_pack(spec, resolved)
    else:
        raise NarrativeError(
            "narrative_unsupported_mission_type",
            "narrative",
            (
                f"narrative.enabled is only supported for mission_type cap, intercept, "
                f"escort, or ground_attack (got {spec.mission_type.value!r})"
            ),
            hint=(
                "Disable narrative, or use mission_type cap, intercept, escort, or ground_attack"
            ),
        )

    return spec.model_copy(
        update={
            "zones": zones,
            "triggers": triggers,
            "narrative": NarrativeSpec(enabled=False),
        }
    )


def _resolved_voice(voice: str | None) -> str:
    resolved = resolve_voice(cli_voice=voice) if voice else DEFAULT_VOICE
    if resolved not in _CAP_COPY:
        return DEFAULT_VOICE
    return resolved


def _apply_cap_pack(spec: MissionSpec, voice: str) -> tuple[list[TriggerZone], list[TriggerRule]]:
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

    copy = _CAP_COPY[voice]
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
    return [zone], triggers


def _apply_intercept_pack(
    spec: MissionSpec, voice: str
) -> tuple[list[TriggerZone], list[TriggerRule]]:
    if not spec.enemies:
        raise NarrativeError(
            "narrative_enemies_required",
            "enemies",
            "Intercept narrative requires at least one enemy flight for the win condition",
        )

    copy = _INTERCEPT_COPY.get(voice, _INTERCEPT_COPY[DEFAULT_VOICE])
    triggers = [
        TriggerRule(
            name="narrative_scramble",
            once=True,
            when=[TimeMoreCondition(seconds=INTERCEPT_SCRAMBLE_SECONDS)],
            then=[MessageAction(text=copy["scramble"], duration_s=12)],
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
    return [], triggers


def _apply_escort_pack(
    spec: MissionSpec, voice: str
) -> tuple[list[TriggerZone], list[TriggerRule]]:
    if spec.escort is None:
        raise NarrativeError(
            "narrative_escort_required",
            "escort",
            "Escort narrative requires a nested escort block",
        )
    if not spec.package:
        raise NarrativeError(
            "narrative_package_required",
            "package",
            "Escort narrative requires a non-empty package list",
        )
    if not spec.enemies:
        raise NarrativeError(
            "narrative_enemies_required",
            "enemies",
            "Escort narrative requires at least one enemy flight for the win condition",
        )

    copy = _ESCORT_COPY.get(voice, _ESCORT_COPY[DEFAULT_VOICE])
    zone = TriggerZone(
        name=ESCORT_DEST_ZONE,
        bearing_deg=spec.escort.bearing_deg,
        distance_km=spec.escort.distance_km,
        radius_m=ESCORT_DEST_RADIUS_M,
    )
    triggers = [
        TriggerRule(
            name="narrative_push",
            once=True,
            when=[TimeMoreCondition(seconds=ESCORT_PUSH_SECONDS)],
            then=[MessageAction(text=copy["push"], duration_s=12)],
        ),
        TriggerRule(
            name="narrative_with_package",
            once=True,
            when=[
                CoalitionInZoneCondition(
                    zone=ESCORT_DEST_ZONE,
                    coalition=spec.player.coalition,
                )
            ],
            then=[MessageAction(text=copy["with_package"], duration_s=12)],
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
    return [zone], triggers


def _apply_ground_attack_pack(
    spec: MissionSpec, voice: str
) -> tuple[list[TriggerZone], list[TriggerRule]]:
    if spec.strike is None:
        raise NarrativeError(
            "narrative_strike_required",
            "strike",
            "Ground-attack narrative requires a nested strike block",
        )
    if not spec.targets:
        raise NarrativeError(
            "narrative_targets_required",
            "targets",
            "Ground-attack narrative requires at least one target for the win condition",
        )

    copy = _GA_COPY.get(voice, _GA_COPY[DEFAULT_VOICE])
    zone = TriggerZone(
        name=STRIKE_AREA_ZONE,
        bearing_deg=spec.strike.bearing_deg,
        distance_km=spec.strike.distance_km,
        radius_m=STRIKE_AREA_RADIUS_M,
    )
    triggers = [
        TriggerRule(
            name="narrative_push",
            once=True,
            when=[TimeMoreCondition(seconds=GA_PUSH_SECONDS)],
            then=[MessageAction(text=copy["push"], duration_s=12)],
        ),
        TriggerRule(
            name="narrative_ingress",
            once=True,
            when=[
                CoalitionInZoneCondition(
                    zone=STRIKE_AREA_ZONE,
                    coalition=spec.player.coalition,
                )
            ],
            then=[MessageAction(text=copy["ingress"], duration_s=12)],
        ),
        TriggerRule(
            name="narrative_targets_down",
            once=True,
            when=[TargetDeadCondition(target_index=0)],
            then=[
                MessageAction(text=copy["win"], duration_s=15),
                MissionEndAction(result=MissionEndResult.WIN),
            ],
        ),
    ]
    return [zone], triggers
