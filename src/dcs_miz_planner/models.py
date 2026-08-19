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
    RECON = "recon"


class Coalition(str, Enum):
    BLUE = "blue"
    RED = "red"


class StartType(str, Enum):
    COLD_PARKING = "cold_parking"  # DCS: TakeOffParking / From Parking Area


class WeatherPreset(str, Enum):
    SUNNY_CLEAR = "sunny_clear"
    DAWN_CLEAR = "dawn_clear"
    SEA_FOG = "sea_fog"
    MARGINAL_VFR = "marginal_vfr"
    LIGHT_SCATTERED_VFR = "light_scattered_vfr"
    HIGH_SCATTERED = "high_scattered"
    BROKEN_CHANNEL = "broken_channel"
    OVERCAST_LOW = "overcast_low"
    RAIN_OVERCAST = "rain_overcast"
    SHOWERS_SCATTERED = "showers_scattered"
    SCATTERED_SUMMER = "scattered_summer"


class WeatherOpts(SpecModel):
    """Invent-time weather options (seed for always-on jitter)."""

    seed: int = Field(ge=0, le=2_147_483_647)


class FogDynamicsMode(str, Enum):
    BURN_OFF = "burn_off"
    ROLL_IN = "roll_in"


class FogDynamics(SpecModel):
    """Mid-sortie fog evolution via curated setFogAnimation (no free-form Lua)."""

    mode: FogDynamicsMode
    start_after_s: int = Field(default=0, ge=0, le=86_400)
    duration_s: int = Field(default=1800, ge=1, le=86_400)
    end_visibility_m: float | None = Field(default=None, ge=0, le=100_000)
    end_thickness_m: float | None = Field(default=None, ge=0, le=5_000)


class FailureEvent(SpecModel):
    """Scheduled player aircraft failure (curated id; ME Failures panel table)."""

    id: str  # exact DCS failure id from Channel catalog
    start_after_s: int = Field(ge=0, le=86_400)  # After time (floored to minutes)
    probability: int = Field(default=100, ge=0, le=100)
    # Maps to ME Within (mm)=minutes; 0 → emit 1 (ED default; Within 0 never fires)
    random_pause_s: int = Field(default=0, ge=0, le=86_400)


class ObjectiveType(str, Enum):
    INTERCEPT_ENEMY = "intercept_enemy"
    PATROL = "patrol"
    ATTACK_GROUND = "attack_ground"
    ESCORT_PACKAGE = "escort_package"
    RECON_AREA = "recon_area"


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


class PlayerFlightRole(str, Enum):
    LEAD = "lead"
    WINGMAN = "wingman"


class SectionOrder(str, Enum):
    """Curated F10 section orders (#15d). No free-form strings."""

    REJOIN = "rejoin"
    ENGAGE = "engage"
    ORBIT = "orbit"
    RTB = "rtb"
    BREAK = "break"


SECTION_ORDER_IDS: frozenset[str] = frozenset(o.value for o in SectionOrder)


class DisciplineHardAction(str, Enum):
    """Curated hard beat when wingman stays outside the section bubble (#15e)."""

    MESSAGE_END = "message_end"
    MISSION_END = "mission_end"
    SECTION_RTB = "section_rtb"


DISCIPLINE_HARD_IDS: frozenset[str] = frozenset(a.value for a in DisciplineHardAction)


class PlayerFlightDiscipline(SpecModel):
    """Opt-in fail-to-follow (omit on flight = off). Empty `{}` uses defaults (= armed)."""

    radius_m: int = Field(default=2500, ge=500)
    soft_after_s: int = Field(default=45, ge=10)
    hard_after_s: int = Field(default=120, ge=10)
    hard: DisciplineHardAction = DisciplineHardAction.MESSAGE_END


class PlayerFlight(SpecModel):
    """Optional multi-ship player section (omit = solo)."""

    size: int = Field(ge=2, le=4)
    role: PlayerFlightRole = PlayerFlightRole.LEAD
    ai_skill: str = "Average"  # AI mates only; not Player/Client
    join_up: bool = True  # wingman: Follow AI lead + shared route (no-op for lead)
    orders: list[SectionOrder] = Field(default_factory=list)  # F10 section orders; omit/[] = none
    discipline: PlayerFlightDiscipline | None = None  # fail-to-follow; omit = off


class Player(SpecModel):
    aircraft: str  # exact DCS type id, e.g. SpitfireLFMkIX
    airfield: str  # display name, mapped to airdromeId by the compiler
    coalition: Coalition = Coalition.BLUE
    country: str = "UK"
    skill: str = "Player"
    start: StartType = StartType.COLD_PARKING
    payload: str | None = None  # named Channel payload preset (ground_attack)
    flight: PlayerFlight | None = None  # multi-ship section; omit = solo


class SceneryObject(SpecModel):
    """Airfield-relative ME static (curated fortification id; no Lua)."""

    type: str
    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(ge=0, le=5)
    heading_deg: float = Field(default=0, ge=0, le=360)


def player_group_size(flight: PlayerFlight | None) -> int:
    """Size of the *player-controlled* flying group.

    Lead (or solo): full section size (1 if omitted).
    Wingman: always 1 — AI lead ships are a separate group (DCS SP cannot put
    Skill=Player on a non-first unit in a mixed group).
    """
    if flight is None:
        return 1
    if flight.role is PlayerFlightRole.WINGMAN:
        return 1
    return int(flight.size)


def player_ai_lead_group_size(flight: PlayerFlight | None) -> int:
    """AI lead section size when role is wingman; otherwise 0."""
    if flight is None or flight.role is not PlayerFlightRole.WINGMAN:
        return 0
    return int(flight.size) - 1


def player_human_unit_index(flight: PlayerFlight | None) -> int:
    """0-based index of Skill=Player within the player flying group (always 0)."""
    _ = flight
    return 0


def player_flight_is_wingman(flight: PlayerFlight | None) -> bool:
    return flight is not None and flight.role is PlayerFlightRole.WINGMAN


def player_flight_join_up_enabled(flight: PlayerFlight | None) -> bool:
    """True when wingman should Follow the AI lead and share the lead's route."""
    return flight is not None and flight.role is PlayerFlightRole.WINGMAN and bool(flight.join_up)


class EnemyFlight(SpecModel):
    """One enemy flight for intercept / CAP opposition."""

    aircraft: str  # exact DCS type id, e.g. Bf-109K-4
    count: int = Field(ge=1, le=16)
    skill: str = "Average"
    country: str = "ThirdReich"
    coalition: Coalition = Coalition.RED
    late_activation: bool = False


class TargetMotion(str, Enum):
    """How a ground/sea target group moves after placement."""

    STATIC = "static"
    PATROL = "patrol"
    PATH = "path"


class TargetPathPoint(SpecModel):
    """One airfield-relative path waypoint for target motion."""

    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(gt=0)


class TargetRoe(str, Enum):
    """Ground/sea ROE (WeaponFree not used for targets)."""

    OPEN_FIRE = "open_fire"
    RETURN_FIRE = "return_fire"
    WEAPONS_HOLD = "weapons_hold"


class TargetAlarmState(str, Enum):
    AUTO = "auto"
    GREEN = "green"
    RED = "red"


class TargetRestrictTargets(str, Enum):
    ALL = "all"
    AIR_ONLY = "air_only"
    GROUND_ONLY = "ground_only"


class TargetMoveFormation(str, Enum):
    """Land waypoint PointAction (not air OptFormation)."""

    OFF_ROAD = "off_road"
    ON_ROAD = "on_road"
    RANK = "rank"
    CONE = "cone"
    VEE = "vee"
    DIAMOND = "diamond"
    ECHELON_LEFT = "echelon_left"
    ECHELON_RIGHT = "echelon_right"


class TargetAi(SpecModel):
    """Allowlisted WP AI options for a ground/sea target (R12 / #15h)."""

    roe: TargetRoe | None = None
    alarm_state: TargetAlarmState | None = None
    engage_air_weapons: bool | None = None
    restrict_targets: TargetRestrictTargets | None = None
    #: Percent 0–100 for OptInterceptionRange (AAA / sea; not soft trucks).
    interception_range: int | None = Field(default=None, ge=0, le=100)


#: Curated preset ids for ``GroundTarget.ai_preset``.
TARGET_AI_PRESETS = frozenset({"convoy_transit", "aaa_alert", "ship_under_way", "harbour_static"})


class GroundTarget(SpecModel):
    """One enemy strike target group (land vehicle or ship/boat).

    Land units belong on enemy-held territory for the mission date (Channel WWII:
    Axis-occupied continent). Mid-Channel / water placements must use sea-domain
    ship ids from the Channel registry — never trucks in the drink.

    Optional motion: omit/`static` = parked; `patrol` + radius; or short looping
    `path` of airfield-relative points (ships under way, truck convoys).

    Optional AI: ``ai_preset`` and/or ``ai`` + land ``move_formation`` (#15h).
    """

    unit: str  # exact DCS ground or ship type id
    count: int = Field(ge=1, le=16)
    skill: str = "Average"
    country: str = "ThirdReich"
    coalition: Coalition = Coalition.RED
    late_activation: bool = False
    motion: TargetMotion | None = None
    patrol_radius_m: float | None = Field(default=None, ge=500, le=15_000)
    path: list[TargetPathPoint] = Field(default_factory=list)
    #: Optional cruise km/h; clamped to the unit's motion profile band when moving.
    speed_kmh: float | None = Field(default=None, gt=0, le=120)
    #: Disperse Under Fire duration (seconds). Omit = auto 180s for moving land;
    #: ``0`` disables; sea units ignore (ground AI option only).
    disperse_under_fire_s: int | None = Field(default=None, ge=0, le=600)
    ai_preset: str | None = None
    ai: TargetAi | None = None
    move_formation: TargetMoveFormation | None = None

    @model_validator(mode="after")
    def _motion_field_rules(self) -> GroundTarget:
        motion = self.motion if self.motion is not None else TargetMotion.STATIC
        if motion is TargetMotion.STATIC:
            if self.patrol_radius_m is not None:
                raise ValueError(
                    "patrol_radius_m only valid when motion is patrol; omit for static"
                )
            if self.path:
                raise ValueError("path only valid when motion is path; omit for static")
            if self.speed_kmh is not None:
                raise ValueError("speed_kmh only valid when motion is patrol or path")
        elif motion is TargetMotion.PATROL:
            if self.patrol_radius_m is None:
                raise ValueError("motion patrol requires patrol_radius_m")
            if self.path:
                raise ValueError("path not valid when motion is patrol")
        else:
            # PATH
            if not (2 <= len(self.path) <= 6):
                raise ValueError("motion path requires 2–6 airfield-relative path points")
            if self.patrol_radius_m is not None:
                raise ValueError("patrol_radius_m not valid when motion is path")
        if self.ai_preset is not None and self.ai_preset not in TARGET_AI_PRESETS:
            raise ValueError(
                f"unknown ai_preset {self.ai_preset!r}; "
                f"allowed: {', '.join(sorted(TARGET_AI_PRESETS))}"
            )
        return self


def ground_target_motion(tgt: GroundTarget) -> TargetMotion:
    """Effective motion mode (omit → static)."""
    return tgt.motion if tgt.motion is not None else TargetMotion.STATIC


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


class Recon(SpecModel):
    """Recon AOI relative to the player departure airfield (observe, not strike)."""

    bearing_deg: float = Field(ge=0, le=360)
    distance_km: float = Field(gt=0)
    altitude_m: float = Field(gt=0)
    radius_m: float = Field(default=3000.0, ge=500, le=15_000)
    mark: bool = True


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


class FlagEqualsCondition(SpecModel):
    type: Literal["flag_equals"] = "flag_equals"
    flag: str = Field(min_length=1)
    value: int


class FlagMoreCondition(SpecModel):
    type: Literal["flag_more"] = "flag_more"
    flag: str = Field(min_length=1)
    value: int


class FlagLessCondition(SpecModel):
    type: Literal["flag_less"] = "flag_less"
    flag: str = Field(min_length=1)
    value: int


class TimeSinceFlagCondition(SpecModel):
    type: Literal["time_since_flag"] = "time_since_flag"
    flag: str = Field(min_length=1)
    seconds: float = Field(gt=0)


class UnitDeadCondition(SpecModel):
    type: Literal["unit_dead"] = "unit_dead"
    enemy_index: int = Field(ge=0, description="0-based index into Spec enemies[]")


class TargetDeadCondition(SpecModel):
    type: Literal["target_dead"] = "target_dead"
    target_index: int = Field(ge=0, description="0-based index into Spec targets[]")


class GroupLifeLessCondition(SpecModel):
    """True when remaining group life is below ``percent`` (ME Group Life Less)."""

    type: Literal["group_life_less"] = "group_life_less"
    enemy_index: int | None = Field(default=None, ge=0)
    target_index: int | None = Field(default=None, ge=0)
    percent: int = Field(ge=1, le=100)

    @model_validator(mode="after")
    def _exactly_one_index(self) -> GroupLifeLessCondition:
        has_e = self.enemy_index is not None
        has_t = self.target_index is not None
        if has_e == has_t:
            raise ValueError("group_life_less requires exactly one of enemy_index or target_index")
        return self


class CoalitionInZoneCondition(SpecModel):
    type: Literal["coalition_in_zone"] = "coalition_in_zone"
    zone: str = Field(min_length=1)
    coalition: Coalition


class UnitAltitudeHigherCondition(SpecModel):
    """True when player unit altitude is above ``altitude_m`` (ME Unit Altitude Higher)."""

    type: Literal["unit_altitude_higher"] = "unit_altitude_higher"
    altitude_m: float = Field(gt=0)
    agl: bool = True


class UnitAltitudeLowerCondition(SpecModel):
    """True when player unit altitude is below ``altitude_m`` (ME Unit Altitude Lower)."""

    type: Literal["unit_altitude_lower"] = "unit_altitude_lower"
    altitude_m: float = Field(gt=0)
    agl: bool = True


class UnitSpeedHigherCondition(SpecModel):
    """True when player unit speed is above ``speed_kmh`` (ME Unit Speed Higher)."""

    type: Literal["unit_speed_higher"] = "unit_speed_higher"
    speed_kmh: float = Field(gt=0)


class UnitSpeedLowerCondition(SpecModel):
    """True when player unit speed is below ``speed_kmh`` (ME Unit Speed Lower)."""

    type: Literal["unit_speed_lower"] = "unit_speed_lower"
    speed_kmh: float = Field(gt=0)


TriggerCondition = Annotated[
    TimeMoreCondition
    | FlagIsCondition
    | FlagEqualsCondition
    | FlagMoreCondition
    | FlagLessCondition
    | TimeSinceFlagCondition
    | UnitDeadCondition
    | TargetDeadCondition
    | GroupLifeLessCondition
    | CoalitionInZoneCondition
    | UnitAltitudeHigherCondition
    | UnitAltitudeLowerCondition
    | UnitSpeedHigherCondition
    | UnitSpeedLowerCondition,
    Field(discriminator="type"),
]


class MessageAction(SpecModel):
    type: Literal["message"] = "message"
    text: str = Field(min_length=1)
    # Non-zero delay is unsupported at emit; keep field only as 0 / omitted.
    delay_s: float = Field(default=0, ge=0, le=0)
    duration_s: float | None = Field(default=None, gt=0)


class SetFlagAction(SpecModel):
    type: Literal["set_flag"] = "set_flag"
    flag: str = Field(min_length=1)
    value: bool


class SetFlagValueAction(SpecModel):
    type: Literal["set_flag_value"] = "set_flag_value"
    flag: str = Field(min_length=1)
    value: int


class IncFlagAction(SpecModel):
    type: Literal["inc_flag"] = "inc_flag"
    flag: str = Field(min_length=1)
    by: int = Field(default=1)


class SetFlagRandomAction(SpecModel):
    """Set a numeric flag to a uniform random integer in [min, max] (ME Set Flag Random)."""

    type: Literal["set_flag_random"] = "set_flag_random"
    flag: str = Field(min_length=1)
    min: int
    max: int

    @model_validator(mode="after")
    def _min_le_max(self) -> SetFlagRandomAction:
        if self.min > self.max:
            raise ValueError("set_flag_random requires min <= max")
        return self


class SoundAction(SpecModel):
    """Play a curated sound asset to all (no arbitrary paths)."""

    type: Literal["sound"] = "sound"
    asset_id: str = Field(min_length=1)


class MissionEndAction(SpecModel):
    type: Literal["mission_end"] = "mission_end"
    result: MissionEndResult


class RadioItemAddAction(SpecModel):
    """Add an F10 radio menu item that sets a named flag on (ME value 1)."""

    type: Literal["radio_item_add"] = "radio_item_add"
    label: str = Field(min_length=1)
    flag: str = Field(min_length=1)
    coalition: Coalition | None = None


class RadioItemRemoveAction(SpecModel):
    type: Literal["radio_item_remove"] = "radio_item_remove"
    label: str = Field(min_length=1)


class ActivateGroupAction(SpecModel):
    """Activate a late-activated enemy or ground-target group by Spec index."""

    type: Literal["activate_group"] = "activate_group"
    enemy_index: int | None = Field(default=None, ge=0)
    target_index: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def _exactly_one_index(self) -> ActivateGroupAction:
        has_e = self.enemy_index is not None
        has_t = self.target_index is not None
        if has_e == has_t:
            raise ValueError("activate_group requires exactly one of enemy_index or target_index")
        return self


class DeactivateGroupAction(SpecModel):
    type: Literal["deactivate_group"] = "deactivate_group"
    enemy_index: int | None = Field(default=None, ge=0)
    target_index: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def _exactly_one_index(self) -> DeactivateGroupAction:
        has_e = self.enemy_index is not None
        has_t = self.target_index is not None
        if has_e == has_t:
            raise ValueError("deactivate_group requires exactly one of enemy_index or target_index")
        return self


class SmokeColor(str, Enum):
    """ME Smoke Marker colors (ExplodeWPMarker)."""

    GREEN = "green"
    RED = "red"
    WHITE = "white"
    ORANGE = "orange"
    BLUE = "blue"


class MarkAction(SpecModel):
    """F10 map mark on a Spec zone (ME Mark To All)."""

    type: Literal["mark"] = "mark"
    zone: str = Field(min_length=1)
    text: str = Field(min_length=1)
    readonly: bool = True


class SmokeAction(SpecModel):
    """Colored smoke pillar on a Spec zone (ME Smoke Marker)."""

    type: Literal["smoke"] = "smoke"
    zone: str = Field(min_length=1)
    color: SmokeColor
    altitude_m: float = Field(default=1.0, gt=0)


TriggerAction = Annotated[
    MessageAction
    | SetFlagAction
    | SetFlagValueAction
    | IncFlagAction
    | SetFlagRandomAction
    | SoundAction
    | MissionEndAction
    | RadioItemAddAction
    | RadioItemRemoveAction
    | ActivateGroupAction
    | DeactivateGroupAction
    | MarkAction
    | SmokeAction,
    Field(discriminator="type"),
]


class TriggerRule(SpecModel):
    """One condition→action rule (AND of ``when``, ordered ``then``). No Lua."""

    name: str | None = None
    once: bool = True
    when: list[TriggerCondition] = Field(min_length=1)
    then: list[TriggerAction] = Field(min_length=1)


class NarrativeSpec(SpecModel):
    """Opt-in immersion pack that expands into typed zones/triggers (no Lua)."""

    enabled: bool = False


class DynamicsMode(str, Enum):
    """Play-time variation mode (Layer B; distinct from CLI randomize)."""

    FIXED = "fixed"
    LIVE = "live"
    CHOOSE = "choose"
    HYBRID = "hybrid"


class DynamicsRoll(SpecModel):
    """Dice parameters for ``live`` / ``hybrid`` Auto paths."""

    flag: str = Field(default="dyn_roll", min_length=1)
    min: int = 1
    max: int = 3
    after_s: float = Field(default=5.0, ge=0)

    @model_validator(mode="after")
    def _min_le_max(self) -> DynamicsRoll:
        if self.min > self.max:
            raise ValueError("dynamics.roll requires min <= max")
        return self


class DynamicsMenu(SpecModel):
    """F10 menu timing / Auto label for ``choose`` / ``hybrid``."""

    after_s: float = Field(default=1.0, ge=0)
    auto_label: str = Field(default="Auto (random)", min_length=1)


class DynamicsPool(SpecModel):
    """One exclusive or selectable opposition / target pool."""

    id: str = Field(min_length=1)
    roll_value: int | None = None
    menu_label: str | None = None
    enemy_indices: list[int] = Field(default_factory=list)
    target_indices: list[int] = Field(default_factory=list)
    message: str | None = None

    @model_validator(mode="after")
    def _has_indices(self) -> DynamicsPool:
        if not self.enemy_indices and not self.target_indices:
            raise ValueError(
                "dynamics pool requires at least one enemy_indices or target_indices entry"
            )
        for idx in self.enemy_indices:
            if idx < 0:
                raise ValueError("enemy_indices must be >= 0")
        for idx in self.target_indices:
            if idx < 0:
                raise ValueError("target_indices must be >= 0")
        return self


class DynamicsSpec(SpecModel):
    """Opt-in play-time variation pack → typed triggers (no Lua).

    Expands before validate/compile when present; cleared after expand (like narrative).
    """

    mode: DynamicsMode
    pools: list[DynamicsPool] = Field(default_factory=list)
    roll: DynamicsRoll | None = None
    menu: DynamicsMenu | None = None
    exclusive: bool = True


def opposing_coalition(coalition: Coalition) -> Coalition:
    return Coalition.RED if coalition is Coalition.BLUE else Coalition.BLUE


class MissionSpec(SpecModel):
    """Declarative mission specification (free flight through recon).

    Optional ``zones`` / ``triggers`` use the typed mission-triggers model (no Lua);
    validated graphs emit as native ME trigger tables. Optional ``narrative.enabled``
    expands a curated pack into zones/triggers before validate/compile. Optional
    ``dynamics`` expands play-time dice/F10/activate graphs the same way.
    Combat extension rules depend on ``mission_type``.
    """

    schema_version: str = Field(description='Mission Spec schema version. Only "1" is supported.')
    mission_type: MissionType = MissionType.FREE_FLIGHT
    theatre: str  # exact DCS theatre id, e.g. TheChannel
    date: MissionDate
    start_time: str  # "HH:MM" 24h; compiler converts to seconds-since-midnight
    weather: WeatherPreset
    weather_opts: WeatherOpts | None = None
    fog_dynamics: FogDynamics | None = None
    failures: list[FailureEvent] = Field(default_factory=list)
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
    recon: Recon | None = None
    narrative: NarrativeSpec | None = None
    dynamics: DynamicsSpec | None = None
    scenery: list[SceneryObject] = Field(default_factory=list)

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
            if self.recon is not None:
                raise ValueError("recon not supported for free_flight: omit the recon block")
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
                    "(use mission_type intercept, cap, ground_attack, escort, or recon)"
                )
            return self

        if self.mission_type is MissionType.INTERCEPT:
            if self.cap is not None:
                raise ValueError("cap not supported for intercept: omit the cap block")
            if self.strike is not None:
                raise ValueError("strike not supported for intercept: omit the strike block")
            if self.escort is not None:
                raise ValueError("escort not supported for intercept: omit the escort block")
            if self.recon is not None:
                raise ValueError("recon not supported for intercept: omit the recon block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for intercept: omit payload")
            if self.targets:
                raise ValueError(
                    "targets not supported for intercept: use mission_type ground_attack or recon"
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
            if self.recon is not None:
                raise ValueError("recon not supported for cap: omit the recon block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for cap: omit payload")
            if self.targets:
                raise ValueError(
                    "targets not supported for cap: use mission_type ground_attack or recon"
                )
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
            if self.recon is not None:
                raise ValueError("recon not supported for ground_attack: omit the recon block")
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
            if self.recon is not None:
                raise ValueError("recon not supported for escort: omit the recon block")
            if self.escort is None:
                raise ValueError("escort missions require a nested escort block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for escort: omit payload")
            if self.targets:
                raise ValueError(
                    "targets not supported for escort: use mission_type ground_attack or recon"
                )
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

        if self.mission_type is MissionType.RECON:
            if self.cap is not None:
                raise ValueError("cap not supported for recon: omit the cap block")
            if self.strike is not None:
                raise ValueError("strike not supported for recon: omit the strike block")
            if self.escort is not None:
                raise ValueError("escort not supported for recon: omit the escort block")
            if self.package:
                raise ValueError("package not supported for recon: use mission_type escort")
            if self.recon is None:
                raise ValueError("recon missions require a nested recon block")
            if self.player.payload is not None:
                raise ValueError("player.payload not supported for recon: omit payload")
            if self.enemies:
                raise ValueError(
                    "air enemies not supported for recon in schema_version 1: use empty enemies"
                )
            if not self.objectives:
                raise ValueError("recon missions require a non-empty objectives list")
            if not any(o.type is ObjectiveType.RECON_AREA for o in self.objectives):
                raise ValueError("recon missions require at least one recon_area objective")
            for i, obj in enumerate(self.objectives):
                if obj.type is not ObjectiveType.RECON_AREA:
                    raise ValueError(
                        f"Unsupported objective type {obj.type.value!r} for recon "
                        "(supported: recon_area)"
                    )
            expected = opposing_coalition(self.player.coalition)
            for i, tgt in enumerate(self.targets):
                if tgt.coalition is not expected:
                    raise ValueError(
                        f"targets[{i}].coalition must be opposing player coalition "
                        f"({self.player.coalition.value!r}; expected {expected.value!r}, "
                        f"got {tgt.coalition.value!r}) — recon contacts are observe-only enemies"
                    )
            return self

        raise ValueError(f"Unsupported mission_type {self.mission_type!r}")  # pragma: no cover

    @property
    def start_seconds(self) -> int:
        hh, mm = (int(p) for p in self.start_time.split(":"))
        return hh * 3600 + mm * 60
