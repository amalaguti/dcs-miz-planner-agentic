"""Mission Spec models — the AI/compiler contract.

Public, backend-agnostic domain model. Never contains PyDCS types.
Scope (v1): free-flight missions only.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

#: Only schema version this build understands. Bump in a future change, never silently.
SCHEMA_VERSION = "1"


class SpecModel(BaseModel):
    """Base for all Mission Spec models: reject unknown/misspelled fields."""

    model_config = ConfigDict(extra="forbid")


class MissionType(str, Enum):
    FREE_FLIGHT = "free_flight"


class Coalition(str, Enum):
    BLUE = "blue"
    RED = "red"


class StartType(str, Enum):
    COLD_PARKING = "cold_parking"  # DCS: TakeOffParking / From Parking Area


class WeatherPreset(str, Enum):
    SUNNY_CLEAR = "sunny_clear"


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


class MissionSpec(SpecModel):
    """Declarative free-flight mission specification.

    ``enemies`` / ``objectives`` / ``triggers`` are reserved extension points for
    future combat and immersion work (backlog M4 / M6). They MUST stay empty in
    this schema version; the compiler ignores them when empty and refuses to
    silently drop non-empty values.
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

    # Reserved extension points — not compiled yet (must be empty in v1).
    enemies: list[Any] = Field(default_factory=list)
    objectives: list[Any] = Field(default_factory=list)
    triggers: list[Any] = Field(default_factory=list)

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
    def _reject_unsupported_extensions(self) -> MissionSpec:
        used = [name for name in ("enemies", "objectives", "triggers") if getattr(self, name)]
        if used:
            raise ValueError(
                f"{', '.join(used)} not supported yet: combat/trigger extension "
                "points are reserved for a future schema version and must be empty"
            )
        return self

    @property
    def start_seconds(self) -> int:
        hh, mm = (int(p) for p in self.start_time.split(":"))
        return hh * 3600 + mm * 60
