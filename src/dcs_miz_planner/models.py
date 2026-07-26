"""Mission Spec models — the AI/compiler contract.

Public, backend-agnostic domain model. Never contains PyDCS types.
Scope: free-flight and intercept (schema_version \"1\").
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

#: Only schema version this build understands. Bump in a future change, never silently.
SCHEMA_VERSION = "1"


class SpecModel(BaseModel):
    """Base for all Mission Spec models: reject unknown/misspelled fields."""

    model_config = ConfigDict(extra="forbid")


class MissionType(str, Enum):
    FREE_FLIGHT = "free_flight"
    INTERCEPT = "intercept"


class Coalition(str, Enum):
    BLUE = "blue"
    RED = "red"


class StartType(str, Enum):
    COLD_PARKING = "cold_parking"  # DCS: TakeOffParking / From Parking Area


class WeatherPreset(str, Enum):
    SUNNY_CLEAR = "sunny_clear"


class ObjectiveType(str, Enum):
    INTERCEPT_ENEMY = "intercept_enemy"


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


class EnemyFlight(SpecModel):
    """One enemy flight for intercept (and later combat types)."""

    aircraft: str  # exact DCS type id, e.g. Bf-109K-4
    count: int = Field(ge=1, le=16)
    skill: str = "Average"
    country: str = "ThirdReich"
    coalition: Coalition = Coalition.RED


class Objective(SpecModel):
    type: ObjectiveType


class MissionSpec(SpecModel):
    """Declarative mission specification (free flight or intercept).

    ``triggers`` remain reserved for M6 and MUST stay empty in this schema version.
    ``enemies`` / ``objectives`` are required for intercept and must stay empty for
    free_flight.
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
    triggers: list[dict] = Field(default_factory=list)

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
        if self.triggers:
            raise ValueError(
                "triggers not supported yet: must be empty in schema_version 1 "
                "(reserved for a future trigger model)"
            )

        if self.mission_type is MissionType.FREE_FLIGHT:
            used = [name for name in ("enemies", "objectives") if getattr(self, name)]
            if used:
                raise ValueError(
                    f"{', '.join(used)} not supported for free_flight: "
                    "combat extension points must be empty (use mission_type intercept)"
                )
            return self

        if self.mission_type is MissionType.INTERCEPT:
            if not self.enemies:
                raise ValueError("intercept missions require a non-empty enemies list")
            if not self.objectives:
                raise ValueError("intercept missions require a non-empty objectives list")
            return self

        raise ValueError(f"Unsupported mission_type {self.mission_type!r}")  # pragma: no cover

    @property
    def start_seconds(self) -> int:
        hh, mm = (int(p) for p in self.start_time.split(":"))
        return hh * 3600 + mm * 60
