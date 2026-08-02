"""Mission Spec models — the AI/compiler contract.

Public, backend-agnostic domain model. Never contains PyDCS types.
Scope: free-flight, intercept, CAP, ground-attack, and escort (schema_version \"1\").
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

#: Only schema version this build understands. Bump in a future change, never silently.
SCHEMA_VERSION = "1"


class SpecModel(BaseModel):
    """Base for all Mission Spec models: reject unknown/misspelled fields."""

    model_config = ConfigDict(extra="forbid")


class MissionType(str, Enum):
    FREE_FLIGHT = "free_flight"
    INTERCEPT = "intercept"
    CAP = "cap"
    GROUND_ATTACK = "ground_attack"
    ESCORT = "escort"


class Coalition(str, Enum):
    BLUE = "blue"
    RED = "red"


class StartType(str, Enum):
    COLD_PARKING = "cold_parking"  # DCS: TakeOffParking / From Parking Area


class WeatherPreset(str, Enum):
    SUNNY_CLEAR = "sunny_clear"
    DAWN_CLEAR = "dawn_clear"
    MARGINAL_VFR = "marginal_vfr"


class ObjectiveType(str, Enum):
    INTERCEPT_ENEMY = "intercept_enemy"
    PATROL = "patrol"
    ATTACK_GROUND = "attack_ground"
    ESCORT_PACKAGE = "escort_package"


class CapPattern(str, Enum):
    CIRCLE = "circle"
    RACE_TRACK = "race_track"


class Engagement(str, Enum):
    WEAPONS_FREE = "weapons_free"
    OPEN_FIRE = "open_fire"
    RETURN_FIRE = "return_fire"
    WEAPONS_HOLD = "weapons_hold"


class MissionDate(SpecModel):
    year: int = Field(ge=1900, le=2100)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)


class Player(SpecModel):
    aircraft: str  # exact DCS type id, e.g. SpitfireLFMkIX
    airfield: str  # display name, mapped to airdromeId by the compiler
    coalition: Coalition = Coalition.BLUE
    country: str = "UK"
    skill: str = "Player"
    start: StartType = StartType.COLD_PARKING
    payload: str | None = None  # named Channel payload preset (ground_attack)


class EnemyFlight(SpecModel):
    """One enemy flight for intercept / CAP opposition."""

    aircraft: str  # exact DCS type id, e.g. Bf-109K-4
    count: int = Field(ge=1, le=16)
    skill: str = "Average"
    country: str = "ThirdReich"
    coalition: Coalition = Coalition.RED


class GroundTarget(SpecModel):
    """One enemy strike target group (land vehicle or ship/boat).

    Land units belong on enemy-held territory for the mission date (Channel WWII:
    Axis-occupied continent). Mid-Channel / water placements must use sea-domain
    ship ids from the Channel registry — never trucks in the drink.
    """

    unit: str  # exact DCS ground or ship type id
    count: int = Field(ge=1, le=16)
    skill: str = "Average"
    country: str = "ThirdReich"
    coalition: Coalition = Coalition.RED


class Cap(SpecModel):
    """CAP patrol station relative to the player departure airfield."""

    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(gt=0)
    altitude_m: float = Field(gt=0)
    pattern: CapPattern = CapPattern.CIRCLE
    engagement: Engagement
    duration_min: int | None = Field(default=None, ge=1)


class Strike(SpecModel):
    """Ground-attack target area relative to the player departure airfield."""

    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(gt=0)
    altitude_m: float = Field(gt=0)
    #: When true, same-coalition / home-territory targets are allowed (bombing practice).
    practice: bool = False


class PackageFlight(SpecModel):
    """One friendly flight in an escort package (same coalition as the player)."""

    aircraft: str  # exact DCS type id, e.g. MosquitoFBMkVI
    count: int = Field(ge=1, le=16)
    skill: str = "Average"
    country: str = "UK"
    coalition: Coalition = Coalition.BLUE


class Escort(SpecModel):
    """Escort package destination relative to the player departure airfield."""

    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(gt=0)
    altitude_m: float = Field(gt=0)
    engagement: Engagement


class Objective(SpecModel):
    type: ObjectiveType


class MissionEndResult(str, Enum):
    WIN = "win"
    LOSE = "lose"


class TriggerZone(SpecModel):
    """Airfield-relative trigger zone (same convention as cap/strike/escort)."""

    name: str = Field(min_length=1)
    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(gt=0)
    radius_m: float = Field(gt=0)


class TimeMoreCondition(SpecModel):
    type: Literal["time_more"] = "time_more"
    seconds: float = Field(ge=0)


class FlagIsCondition(SpecModel):
    type: Literal["flag_is"] = "flag_is"
    flag: str = Field(min_length=1)
    value: bool


class UnitDeadCondition(SpecModel):
    type: Literal["unit_dead"] = "unit_dead"
    enemy_index: int = Field(ge=0, description="0-based index into Spec enemies[]")


class CoalitionInZoneCondition(SpecModel):
    type: Literal["coalition_in_zone"] = "coalition_in_zone"
    zone: str = Field(min_length=1)
    coalition: Coalition


TriggerCondition = Annotated[
    TimeMoreCondition | FlagIsCondition | UnitDeadCondition | CoalitionInZoneCondition,
    Field(discriminator="type"),
]


class MessageAction(SpecModel):
    type: Literal["message"] = "message"
    text: str = Field(min_length=1)
    delay_s: float = Field(default=0, ge=0)
    duration_s: float | None = Field(default=None, gt=0)


class SetFlagAction(SpecModel):
    type: Literal["set_flag"] = "set_flag"
    flag: str = Field(min_length=1)
    value: bool


class MissionEndAction(SpecModel):
    type: Literal["mission_end"] = "mission_end"
    result: MissionEndResult


TriggerAction = Annotated[
    MessageAction | SetFlagAction | MissionEndAction,
    Field(discriminator="type"),
]


class TriggerRule(SpecModel):
    """One condition→action rule (AND of ``when``, ordered ``then``). No Lua."""

    name: str | None = None
    once: bool = True
    when: list[TriggerCondition] = Field(min_length=1)
    then: list[TriggerAction] = Field(min_length=1)


def opposing_coalition(coalition: Coalition) -> Coalition:
    return Coalition.RED if coalition is Coalition.BLUE else Coalition.BLUE


class MissionSpec(SpecModel):
    """Declarative mission specification (free flight through escort).

    Optional ``zones`` / ``triggers`` use the typed mission-triggers model (no Lua).
    Native ``.miz`` emit for non-empty triggers is deferred to trigger-compiler-native.
    Combat extension rules depend on ``mission_type``.
    """

    schema_version: str = Field(description='Mission Spec schema version. Only "1" is supported.')
    mission_type: MissionType = MissionType.FREE_FLIGHT
    theatre: str  # exact DCS theatre id, e.g. TheChannel
    date: MissionDate
    start_time: str  # "HH:MM" 24h; compiler converts to seconds-since-midnight
    weather: WeatherPreset
    player: Player
    name: str = "Free Flight"
    description: str = ""

    enemies: list[EnemyFlight] = Field(default_factory=list)
    objectives: list[Objective] = Field(default_factory=list)
    zones: list[TriggerZone] = Field(default_factory=list)
    triggers: list[TriggerRule] = Field(default_factory=list)
    targets: list[GroundTarget] = Field(default_factory=list)
    package: list[PackageFlight] = Field(default_factory=list)
    cap: Cap | None = None
    strike: Strike | None = None
    escort: Escort | None = None

    @field_validator("schema_version")
    @classmethod
    def _supported_version(cls, v: str) -> str:
        if v != SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported schema_version {v!r}; this build supports {SCHEMA_VERSION!r} only"
            )
        return v

    @field_validator("start_time")
    @classmethod
    def _valid_hhmm(cls, v: str) -> str:
        parts = v.split(":")
        if len(parts) != 2:
            raise ValueError("start_time must be 'HH:MM'")
        hh, mm = int(parts[0]), int(parts[1])
        if not (0 <= hh < 24 and 0 <= mm < 60):
            raise ValueError("start_time out of range")
        return v

    @model_validator(mode="after")
    def _mission_type_extension_rules(self) -> MissionSpec:
        names = [z.name for z in self.zones]
        if len(names) != len(set(names)):
            raise ValueError("zones must have unique names")

        if self.mission_type is MissionType.FREE_FLIGHT:
            if self.cap is not None:
                raise ValueError("cap not supported for free_flight: omit the cap block")
            if self.strike is not None:
                raise ValueError("strike not supported for free_flight: omit the strike block")
            if self.escort is not None:
                raise ValueError("escort not supported for free_flight: omit the escort block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for free_flight: omit payload")
            used = [
                name
                for name in ("enemies", "objectives", "targets", "package")
                if getattr(self, name)
            ]
            if used:
                raise ValueError(
                    f"{', '.join(used)} not supported for free_flight: "
                    "combat extension points must be empty "
                    "(use mission_type intercept, cap, ground_attack, or escort)"
                )
            return self

        if self.mission_type is MissionType.INTERCEPT:
            if self.cap is not None:
                raise ValueError("cap not supported for intercept: omit the cap block")
            if self.strike is not None:
                raise ValueError("strike not supported for intercept: omit the strike block")
            if self.escort is not None:
                raise ValueError("escort not supported for intercept: omit the escort block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for intercept: omit payload")
            if self.targets:
                raise ValueError(
                    "targets not supported for intercept: use mission_type ground_attack"
                )
            if self.package:
                raise ValueError("package not supported for intercept: use mission_type escort")
            if not self.enemies:
                raise ValueError("intercept missions require a non-empty enemies list")
            if not self.objectives:
                raise ValueError("intercept missions require a non-empty objectives list")
            return self

        if self.mission_type is MissionType.CAP:
            if self.strike is not None:
                raise ValueError("strike not supported for cap: omit the strike block")
            if self.escort is not None:
                raise ValueError("escort not supported for cap: omit the escort block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for cap: omit payload")
            if self.targets:
                raise ValueError("targets not supported for cap: use mission_type ground_attack")
            if self.package:
                raise ValueError("package not supported for cap: use mission_type escort")
            if self.cap is None:
                raise ValueError("cap missions require a nested cap block")
            if not self.objectives:
                raise ValueError("cap missions require a non-empty objectives list")
            if not any(o.type is ObjectiveType.PATROL for o in self.objectives):
                raise ValueError("cap missions require at least one patrol objective")
            return self

        if self.mission_type is MissionType.GROUND_ATTACK:
            if self.cap is not None:
                raise ValueError("cap not supported for ground_attack: omit the cap block")
            if self.escort is not None:
                raise ValueError("escort not supported for ground_attack: omit the escort block")
            if self.package:
                raise ValueError("package not supported for ground_attack: use mission_type escort")
            if self.strike is None:
                raise ValueError("ground_attack missions require a nested strike block")
            if not self.targets:
                raise ValueError("ground_attack missions require a non-empty targets list")
            if self.enemies:
                raise ValueError(
                    "air enemies not supported for ground_attack in schema_version 1: "
                    "use empty enemies"
                )
            if self.player.payload is None or not str(self.player.payload).strip():
                raise ValueError("ground_attack missions require player.payload (named preset)")
            if not self.objectives:
                raise ValueError("ground_attack missions require a non-empty objectives list")
            if not any(o.type is ObjectiveType.ATTACK_GROUND for o in self.objectives):
                raise ValueError(
                    "ground_attack missions require at least one attack_ground objective"
                )
            assert self.strike is not None
            if not self.strike.practice:
                expected = opposing_coalition(self.player.coalition)
                for i, tgt in enumerate(self.targets):
                    if tgt.coalition is not expected:
                        raise ValueError(
                            f"targets[{i}].coalition must be enemy-only "
                            f"(opposing player coalition {self.player.coalition.value!r}; "
                            f"expected {expected.value!r}, got {tgt.coalition.value!r}). "
                            f"Set strike.practice true for allied bombing-practice targets."
                        )
            return self

        if self.mission_type is MissionType.ESCORT:
            if self.cap is not None:
                raise ValueError("cap not supported for escort: omit the cap block")
            if self.strike is not None:
                raise ValueError("strike not supported for escort: omit the strike block")
            if self.escort is None:
                raise ValueError("escort missions require a nested escort block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for escort: omit payload")
            if self.targets:
                raise ValueError("targets not supported for escort: use mission_type ground_attack")
            if not self.package:
                raise ValueError("escort missions require a non-empty package list")
            if not self.objectives:
                raise ValueError("escort missions require a non-empty objectives list")
            if not any(o.type is ObjectiveType.ESCORT_PACKAGE for o in self.objectives):
                raise ValueError("escort missions require at least one escort_package objective")
            for i, flight in enumerate(self.package):
                if flight.coalition is not self.player.coalition:
                    raise ValueError(
                        f"package[{i}].coalition must match player coalition "
                        f"({self.player.coalition.value!r}); got {flight.coalition.value!r} "
                        "(escort package must be friendly)"
                    )
            return self

        raise ValueError(f"Unsupported mission_type {self.mission_type!r}")  # pragma: no cover

    @property
    def start_seconds(self) -> int:
        hh, mm = (int(p) for p in self.start_time.split(":"))
        return hh * 3600 + mm * 60
