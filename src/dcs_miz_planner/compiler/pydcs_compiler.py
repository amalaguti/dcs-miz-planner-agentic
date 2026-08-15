"""PyDCS-backed compiler for free-flight through recon missions.

Boundary rule: this module is the only place allowed to import PyDCS.
The rest of the app depends on `MissionSpec` and `CompilerInterface`.
"""

from __future__ import annotations

import datetime
from pathlib import Path

from ..install.models import TheatreInventory
from ..models import (
    CapPattern,
    Engagement,
    MissionSpec,
    MissionType,
    StartType,
    player_ai_lead_group_size,
    player_flight_is_wingman,
    player_flight_join_up_enabled,
    player_group_size,
)
from ..registry import RegistryError, get_channel_registry
from ..validation import MissionValidationError, validate_mission_spec
from .base import CompilerInterface

# Enemy spawn for the checked-in Manston dawn intercept example.
# Source: PyDCS `TheChannel` airport Hawkinge (airdromeId 6) map position, offset
# south-east toward the Strait as a Dover-approach corridor (Channel geography
# relative to Manston id 5). Not invented lat/lon — terrain units from PyDCS.
_HAWKINGE_X = 26989.935547
_HAWKINGE_Y = -29402.577148
_DOVER_APPROACH_OFFSET_X = 4000.0
_DOVER_APPROACH_OFFSET_Y = -6000.0
_ENEMY_ALTITUDE_M = 3500
_ENEMY_SPEED_KMH = 450

# CAP opposition near the patrol station (station-relative, metres).
_CAP_ENEMY_OFFSET_M_X = 3000.0
_CAP_ENEMY_OFFSET_M_Y = -2000.0
_CAP_RACE_TRACK_LEG_M = 10000.0
_CAP_ORBIT_SPEED_KMH = 400

# Ground-attack ingress / attack speeds (km/h).
_GA_SPEED_KMH = 400
# Spread soft targets slightly around the strike point (metres).
_GA_TARGET_SPREAD_M = 80.0

# Escort package / bounce (metres and km/h).
_ESCORT_SPEED_KMH = 400
_ESCORT_PACKAGE_START_M = 8000.0
_ESCORT_BOUNCE_OFFSET_M_X = 2500.0
_ESCORT_BOUNCE_OFFSET_M_Y = -1500.0

# Recon ingress (km/h) and contact spread (metres).
_RECON_SPEED_KMH = 400
_RECON_CONTACT_SPREAD_M = 80.0

# Wingman join-up: AI lead outbound + player Follow (metres / km/h).
_JOINUP_OUTBOUND_BEARING_DEG = 120.0
_JOINUP_OUTBOUND_M = 12_000.0
_JOINUP_CLIMB_M = 5_000.0
_JOINUP_JOIN_M = 8_000.0
_JOINUP_ALT_M = 1500.0
_JOINUP_SPEED_KMH = 400
_JOINUP_FOLLOW_OFFSET_X = -200.0
_JOINUP_FOLLOW_ALT_DIFF_M = -100.0


def _disable_payload_scan(*unit_types) -> None:
    """Work around a PyDCS bug when a real DCS install is present.

    ``load_payloads`` indexes ``_payload_cache[path]`` for payload files that
    ``scan_payload_dir`` skipped (files without a ``["unitType"]`` line),
    raising ``KeyError``. Free-flight missions need no payloads, so we mark the
    cache non-empty (skip scanning the install) and give each used type an empty
    payload set (early-return before the buggy loop). Ground-attack still disables
    scanning and applies registry CLSIDs manually via ``load_pylon``.
    """
    from dcs.unittype import FlyingType

    if not FlyingType._payload_cache:
        FlyingType._payload_cache = {"__noscan__": "__noscan__"}
    for unit_type in unit_types:
        if getattr(unit_type, "payloads", None) is None:
            unit_type.payloads = {}


def _skill_from_name(name: str):
    from dcs.unit import Skill

    try:
        return Skill[name]
    except KeyError as exc:
        raise ValueError(f"Unknown skill {name!r}") from exc


def _opt_roe_value(engagement: Engagement):
    from dcs.task import OptROE

    return {
        Engagement.WEAPONS_FREE: OptROE.Values.WeaponFree,
        Engagement.OPEN_FIRE: OptROE.Values.OpenFire,
        Engagement.RETURN_FIRE: OptROE.Values.ReturnFire,
        Engagement.WEAPONS_HOLD: OptROE.Values.WeaponHold,
    }[engagement]


class PyDCSCompiler(CompilerInterface):
    """Compile a Mission Spec into a .miz via PyDCS."""

    def __init__(self, *, inventory: TheatreInventory | None = None) -> None:
        # Optional inject for tests; production uses the SQLite install cache.
        self._inventory = inventory

    def compile(
        self,
        spec: MissionSpec,
        output_path: str | Path,
        *,
        voice: str | None = None,
    ) -> Path:
        # Imports are local so the boundary is explicit and importing our
        # package never eagerly pulls PyDCS.
        from dcs import countries
        from dcs.mission import Mission
        from dcs.mission import StartType as DcsStartType
        from dcs.planes import plane_map

        from ..dynamics import DynamicsError, expand_dynamics_if_needed
        from ..narrative import NarrativeError, expand_narrative_if_needed
        from ..theatre_terrain import TheatreTerrainError, terrain_for_theatre

        try:
            spec = expand_narrative_if_needed(spec, voice=voice)
            spec = expand_dynamics_if_needed(spec)
        except (NarrativeError, DynamicsError) as exc:
            raise ValueError(f"{exc.path}: {exc.message}") from exc

        self._validate(spec)

        if spec.mission_type is MissionType.RECON:
            from ..recon import expand_recon_find_pack

            spec = expand_recon_find_pack(spec)

        aircraft_type = plane_map.get(spec.player.aircraft)
        if aircraft_type is None:
            raise ValueError(f"Unknown PyDCS plane id: {spec.player.aircraft}")

        enemy_types = []
        for enemy in spec.enemies:
            et = plane_map.get(enemy.aircraft)
            if et is None:
                raise ValueError(f"Unknown PyDCS plane id: {enemy.aircraft}")
            enemy_types.append(et)

        package_types = []
        for flight in spec.package:
            pt = plane_map.get(flight.aircraft)
            if pt is None:
                raise ValueError(f"Unknown PyDCS plane id: {flight.aircraft}")
            package_types.append(pt)

        _disable_payload_scan(aircraft_type, *enemy_types, *package_types)

        try:
            terrain = terrain_for_theatre(spec.theatre)
        except TheatreTerrainError as exc:
            raise ValueError(str(exc)) from exc

        mission = Mission(terrain=terrain)

        # Date + time. PyDCS start_time is a datetime; DCS mission time is
        # naive local mission time (no timezone).
        mission.start_time = datetime.datetime(  # noqa: DTZ001
            spec.date.year,
            spec.date.month,
            spec.date.day,
            spec.start_seconds // 3600,
            (spec.start_seconds % 3600) // 60,
        )

        self._apply_weather(mission, spec)

        country = self._ensure_country(
            mission, countries, spec.player.country, spec.player.coalition.value
        )

        registry = get_channel_registry()
        try:
            airport_id = registry.airdrome_id(spec.player.airfield, theatre=spec.theatre)
            radio_mhz = registry.radio_mhz(spec.player.aircraft)
        except RegistryError as exc:
            raise ValueError(str(exc)) from exc

        airport = mission.terrain.airport_by_id(airport_id)
        if airport is None:
            raise ValueError(f"Airport not found for {spec.player.airfield}")

        start_type_map = {StartType.COLD_PARKING: DcsStartType.Cold}
        start_type = start_type_map[spec.player.start]

        flight = spec.player.flight
        human_skill = _skill_from_name(spec.player.skill)
        mate_skill = _skill_from_name(flight.ai_skill if flight is not None else "Average")

        # Wingman: separate AI lead group + size-1 Player group. DCS single-player
        # only hands control to Skill=Player on the first unit of a group — putting
        # Player on units[1+] leaves the human as a spectator while AI flies.
        lead_group = None
        if player_flight_is_wingman(flight):
            lead_size = player_ai_lead_group_size(flight)
            lead_group = mission.flight_group_from_airport(
                country=country,
                name=f"{spec.name} Lead",
                aircraft_type=aircraft_type,
                airport=airport,
                start_type=start_type,
                group_size=lead_size,
            )
            for unit in lead_group.units:
                unit.skill = mate_skill
            lead_group.frequency = radio_mhz

            group = mission.flight_group_from_airport(
                country=country,
                name=spec.name,
                aircraft_type=aircraft_type,
                airport=airport,
                start_type=start_type,
                group_size=1,
            )
            group.units[0].skill = human_skill
            group.frequency = radio_mhz
        else:
            group_size = player_group_size(flight)
            group = mission.flight_group_from_airport(
                country=country,
                name=spec.name,
                aircraft_type=aircraft_type,
                airport=airport,
                start_type=start_type,
                group_size=group_size,
            )
            for i, unit in enumerate(group.units):
                unit.skill = human_skill if i == 0 else mate_skill
            group.frequency = radio_mhz

        join_up = player_flight_join_up_enabled(flight)
        task_group = lead_group if join_up else group
        assert task_group is not None

        if join_up:
            assert lead_group is not None
            if spec.mission_type is MissionType.FREE_FLIGHT:
                self._apply_wingman_lead_outbound(lead_group, airport)
            elif spec.mission_type is MissionType.INTERCEPT:
                # Intercept has no player route today — give the lead a short leg
                # so Follow has a moving section to join after scramble.
                self._apply_wingman_lead_outbound(lead_group, airport)
            self._apply_player_follow_lead(group, lead_group, airport)

        enemy_group_ids: list[int] = []
        target_group_ids: list[int] = []
        if spec.mission_type is MissionType.INTERCEPT:
            enemy_group_ids = self._place_enemies(mission, countries, registry, spec, enemy_types)
        elif spec.mission_type is MissionType.CAP:
            self._apply_cap(mission, task_group, airport, spec)
            if spec.enemies:
                enemy_group_ids = self._place_cap_enemies(
                    mission, countries, registry, spec, enemy_types, airport
                )
        elif spec.mission_type is MissionType.GROUND_ATTACK:
            target_group_ids = self._apply_ground_attack(
                mission, countries, registry, task_group, airport, spec
            )
        elif spec.mission_type is MissionType.ESCORT:
            enemy_group_ids = self._apply_escort(
                mission,
                countries,
                registry,
                task_group,
                airport,
                spec,
                package_types,
                enemy_types,
            )
        elif spec.mission_type is MissionType.RECON:
            target_group_ids = self._apply_recon(
                mission, countries, registry, task_group, airport, spec
            )

        self._apply_zones_and_triggers(
            mission,
            airport,
            spec,
            enemy_group_ids,
            target_group_ids,
            player_unit_id=group.units[0].id,
        )
        self._apply_section_orders(
            mission, spec, player_group=group, lead_group=lead_group, airport=airport
        )
        self._apply_flight_discipline(
            mission, spec, player_group=group, lead_group=lead_group, airport=airport
        )
        self._apply_fog_dynamics(mission, spec)
        self._apply_aircraft_failures(mission, spec)
        self._apply_briefing(mission, spec, voice)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        mission.save(str(out))
        self._ensure_theatre_member(out, spec.theatre)
        return out

    @staticmethod
    def _apply_fog_dynamics(mission, spec: MissionSpec) -> None:
        from .fog_emit import apply_fog_dynamics

        apply_fog_dynamics(mission, spec)

    @staticmethod
    def _apply_aircraft_failures(mission, spec: MissionSpec) -> None:
        from .failures_emit import apply_aircraft_failures

        apply_aircraft_failures(mission, spec)

    @staticmethod
    def _apply_section_orders(
        mission,
        spec: MissionSpec,
        *,
        player_group,
        lead_group,
        airport,
    ) -> None:
        from .section_orders_emit import apply_section_orders

        apply_section_orders(
            mission,
            spec,
            player_group=player_group,
            lead_group=lead_group,
            airport=airport,
        )

    @staticmethod
    def _apply_flight_discipline(
        mission,
        spec: MissionSpec,
        *,
        player_group,
        lead_group,
        airport,
    ) -> None:
        from .discipline_emit import apply_flight_discipline

        apply_flight_discipline(
            mission,
            spec,
            player_group=player_group,
            lead_group=lead_group,
            airport=airport,
        )

    @staticmethod
    def _apply_wingman_lead_outbound(lead_group, airport) -> None:
        """Give the AI lead a short outbound leg so Follow has a moving target."""
        outbound = airport.position.point_from_heading(
            _JOINUP_OUTBOUND_BEARING_DEG, _JOINUP_OUTBOUND_M
        )
        lead_group.add_waypoint(
            outbound,
            altitude=_JOINUP_ALT_M,
            speed=_JOINUP_SPEED_KMH,
            name="Section outbound",
        )

    @staticmethod
    def _apply_player_follow_lead(player_group, lead_group, airport) -> None:
        """Climb then Follow the AI lead (cold-start Follow engages after airborne)."""
        from dcs.mapping import Vector2
        from dcs.task import Follow

        player_group.add_waypoint(
            airport.position.point_from_heading(_JOINUP_OUTBOUND_BEARING_DEG, _JOINUP_CLIMB_M),
            altitude=_JOINUP_ALT_M,
            speed=_JOINUP_SPEED_KMH,
            name="Climb",
        )
        join_wp = player_group.add_waypoint(
            airport.position.point_from_heading(_JOINUP_OUTBOUND_BEARING_DEG, _JOINUP_JOIN_M),
            altitude=_JOINUP_ALT_M,
            speed=_JOINUP_SPEED_KMH,
            name="Join",
        )
        join_wp.add_task(
            Follow(
                groupid=lead_group.id,
                group_offset=Vector2(_JOINUP_FOLLOW_OFFSET_X, 0.0),
                altitude_difference=_JOINUP_FOLLOW_ALT_DIFF_M,
            )
        )

    @staticmethod
    def _apply_zones_and_triggers(
        mission,
        airport,
        spec: MissionSpec,
        enemy_group_ids: list[int],
        target_group_ids: list[int] | None = None,
        player_unit_id: int | None = None,
    ) -> None:
        from .triggers_emit import apply_zones_and_triggers

        apply_zones_and_triggers(
            mission,
            airport,
            spec,
            enemy_group_ids,
            target_group_ids=target_group_ids,
            player_unit_id=player_unit_id,
        )

    @staticmethod
    def _apply_briefing(mission, spec: MissionSpec, voice: str | None) -> None:
        """Write Sortie / Description / Task strings into mission ``l10n``."""
        from ..briefing import build_mission_briefing_texts

        texts = build_mission_briefing_texts(spec, voice)
        mission.set_sortie_text(texts.sortie)
        mission.set_description_text(texts.description)
        mission.set_description_bluetask_text(texts.blue_task)
        mission.set_description_redtask_text(texts.red_task)

    @staticmethod
    def _ensure_country(mission, countries_mod, country_name: str, coalition: str):
        """Add/find a PyDCS country on the requested coalition.

        Spec uses the PyDCS class attribute name (``UK``, ``ThirdReich``). Lookup in
        the mission uses the DCS display name (``UK``, ``Third Reich``). Modern
        ``Germany`` is already on blue in Channel defaults — WWII Axis must use
        ``ThirdReich`` on red, or bandits appear as Allies.
        """
        country_cls = getattr(countries_mod, country_name, None)
        if country_cls is None:
            raise ValueError(f"Unknown country: {country_name}")

        dcs_name = country_cls.name
        existing = mission.country(dcs_name)
        if existing is not None:
            for side, coal in mission.coalition.items():
                if dcs_name in coal.countries:
                    if side != coalition:
                        raise ValueError(
                            f"Country {country_name!r} ({dcs_name}) is already on "
                            f"coalition {side!r}; cannot place on {coalition!r}. "
                            f"For WWII Axis use country ThirdReich on red, not Germany."
                        )
                    return existing
            return existing

        mission.coalition[coalition].add_country(country_cls())
        country = mission.country(dcs_name)
        if country is None:
            raise ValueError(f"Failed to add country: {country_name}")
        return country

    def _apply_cap(self, mission, group, airport, spec: MissionSpec) -> None:
        from dcs.task import CAP, ControlledTask, OptROE, OrbitAction

        del mission  # station uses airport.position / terrain via Point
        assert spec.cap is not None
        cap = spec.cap
        group.task = CAP.name

        station = airport.position.point_from_heading(cap.bearing_deg, cap.distance_km * 1000.0)
        group.add_waypoint(
            airport.position.point_from_heading(cap.bearing_deg, 5000.0),
            altitude=min(cap.altitude_m, 1500.0),
            speed=_CAP_ORBIT_SPEED_KMH,
            name="Climb",
        )

        pattern = (
            OrbitAction.OrbitPattern.Circle
            if cap.pattern is CapPattern.CIRCLE
            else OrbitAction.OrbitPattern.RaceTrack
        )
        orbit = OrbitAction(
            altitude=cap.altitude_m,
            speed=_CAP_ORBIT_SPEED_KMH,
            pattern=pattern,
        )
        if cap.duration_min is not None:
            controlled = ControlledTask(orbit)
            controlled.stop_after_duration(int(cap.duration_min) * 60)
            orbit_task = controlled
        else:
            orbit_task = orbit

        cap_wp = group.add_waypoint(
            station,
            altitude=cap.altitude_m,
            speed=_CAP_ORBIT_SPEED_KMH,
            name="CAP",
        )
        cap_wp.add_task(orbit_task)
        cap_wp.add_task(OptROE(_opt_roe_value(cap.engagement)))

        if cap.pattern is CapPattern.RACE_TRACK:
            # Second point defines the race-track long axis (~10 km along bearing).
            leg = station.point_from_heading(cap.bearing_deg, _CAP_RACE_TRACK_LEG_M)
            group.add_waypoint(
                leg,
                altitude=cap.altitude_m,
                speed=_CAP_ORBIT_SPEED_KMH,
                name="CAP leg",
            )

    def _apply_ground_attack(
        self,
        mission,
        countries_mod,
        registry,
        group,
        airport,
        spec: MissionSpec,
    ) -> list[int]:
        from dcs.mapping import Vector2
        from dcs.task import Bombing, GroundAttack, OptJettisonEmptyTanks

        assert spec.strike is not None
        assert spec.player.payload is not None
        strike = spec.strike
        group.task = GroundAttack.name

        try:
            payload = registry.get_payload(spec.player.payload)
        except RegistryError as exc:
            raise ValueError(str(exc)) from exc

        for pylon_ref in payload.pylons:
            group.load_pylon((pylon_ref.pylon, {"clsid": pylon_ref.clsid}))

        target = airport.position.point_from_heading(
            strike.bearing_deg, strike.distance_km * 1000.0
        )
        group.add_waypoint(
            airport.position.point_from_heading(strike.bearing_deg, 5000.0),
            altitude=min(strike.altitude_m, 1500.0),
            speed=_GA_SPEED_KMH,
            name="Climb",
        )
        ip = group.add_waypoint(
            airport.position.point_from_heading(
                strike.bearing_deg, max(strike.distance_km * 1000.0 - 8000.0, 8000.0)
            ),
            altitude=strike.altitude_m,
            speed=_GA_SPEED_KMH,
            name="IP",
        )
        # Allow cockpit jettison of the slipper; empty-tank auto-jettison for AI hygiene.
        # Do not set OptRestrictJettison.
        ip.add_task(OptJettisonEmptyTanks(True))

        tgt_wp = group.add_waypoint(
            target,
            altitude=strike.altitude_m,
            speed=_GA_SPEED_KMH,
            name="Target",
        )
        tgt_wp.add_task(Bombing(Vector2(target.x, target.y), altitude=int(strike.altitude_m)))

        group_ids: list[int] = []
        for i, tgt in enumerate(spec.targets):
            strike_unit = registry.get_strike_unit(tgt.unit)
            country = self._ensure_country(mission, countries_mod, tgt.country, tgt.coalition.value)
            # Slight lateral offset so multi-unit groups are not stacked on one point.
            fallback = target.point_from_heading(90.0 + i * 25.0, _GA_TARGET_SPREAD_M * (i + 1))
            from ..target_motion import (
                apply_target_motion,
                motion_seed_for_spec,
                spawn_position_for_target,
            )

            pos = spawn_position_for_target(
                airport_position=airport.position,
                area_center=target,
                tgt=tgt,
                fallback_pos=fallback,
            )
            skill = _skill_from_name(tgt.skill)
            if strike_unit.domain == "sea":
                from dcs.ships import ship_map

                ship_type = ship_map.get(tgt.unit)
                if ship_type is None:
                    raise ValueError(f"Unknown PyDCS ship id: {tgt.unit}")
                sg = mission.ship_group(
                    country=country,
                    name=f"Target {tgt.unit}",
                    _type=ship_type,
                    position=pos,
                    group_size=tgt.count,
                )
                for unit in sg.units:
                    unit.skill = skill
                if tgt.late_activation:
                    sg.late_activation = True
                apply_target_motion(
                    sg,
                    airport_position=airport.position,
                    area_center=target,
                    tgt=tgt,
                    domain="sea",
                    seed=motion_seed_for_spec(spec),
                    target_index=i,
                )
                group_ids.append(sg.id)
            else:
                from dcs.vehicles import vehicle_map

                vehicle_type = vehicle_map.get(tgt.unit)
                if vehicle_type is None:
                    raise ValueError(f"Unknown PyDCS vehicle id: {tgt.unit}")
                vg = mission.vehicle_group(
                    country=country,
                    name=f"Target {tgt.unit}",
                    _type=vehicle_type,
                    position=pos,
                    group_size=tgt.count,
                )
                for unit in vg.units:
                    unit.skill = skill
                if tgt.late_activation:
                    vg.late_activation = True
                apply_target_motion(
                    vg,
                    airport_position=airport.position,
                    area_center=target,
                    tgt=tgt,
                    domain="land",
                    seed=motion_seed_for_spec(spec),
                    target_index=i,
                )
                group_ids.append(vg.id)
        return group_ids

    def _apply_recon(
        self,
        mission,
        countries_mod,
        registry,
        group,
        airport,
        spec: MissionSpec,
    ) -> list[int]:
        from dcs.task import OptROE, Reconnaissance

        assert spec.recon is not None
        recon = spec.recon
        group.task = Reconnaissance.name

        aoi = airport.position.point_from_heading(recon.bearing_deg, recon.distance_km * 1000.0)
        group.add_waypoint(
            airport.position.point_from_heading(recon.bearing_deg, 5000.0),
            altitude=min(recon.altitude_m, 1500.0),
            speed=_RECON_SPEED_KMH,
            name="Climb",
        )
        observe = group.add_waypoint(
            aoi,
            altitude=recon.altitude_m,
            speed=_RECON_SPEED_KMH,
            name="Observe",
        )
        observe.add_task(OptROE(_opt_roe_value(Engagement.WEAPONS_HOLD)))

        group_ids: list[int] = []
        for i, tgt in enumerate(spec.targets):
            strike_unit = registry.get_strike_unit(tgt.unit)
            country = self._ensure_country(mission, countries_mod, tgt.country, tgt.coalition.value)
            fallback = aoi.point_from_heading(90.0 + i * 25.0, _RECON_CONTACT_SPREAD_M * (i + 1))
            from ..target_motion import (
                apply_target_motion,
                motion_seed_for_spec,
                spawn_position_for_target,
            )

            pos = spawn_position_for_target(
                airport_position=airport.position,
                area_center=aoi,
                tgt=tgt,
                fallback_pos=fallback,
            )
            skill = _skill_from_name(tgt.skill)
            if strike_unit.domain == "sea":
                from dcs.ships import ship_map

                ship_type = ship_map.get(tgt.unit)
                if ship_type is None:
                    raise ValueError(f"Unknown PyDCS ship id: {tgt.unit}")
                sg = mission.ship_group(
                    country=country,
                    name=f"Contact {tgt.unit}",
                    _type=ship_type,
                    position=pos,
                    group_size=tgt.count,
                )
                for unit in sg.units:
                    unit.skill = skill
                if tgt.late_activation:
                    sg.late_activation = True
                apply_target_motion(
                    sg,
                    airport_position=airport.position,
                    area_center=aoi,
                    tgt=tgt,
                    domain="sea",
                    seed=motion_seed_for_spec(spec),
                    target_index=i,
                )
                group_ids.append(sg.id)
            else:
                from dcs.vehicles import vehicle_map

                vehicle_type = vehicle_map.get(tgt.unit)
                if vehicle_type is None:
                    raise ValueError(f"Unknown PyDCS vehicle id: {tgt.unit}")
                vg = mission.vehicle_group(
                    country=country,
                    name=f"Contact {tgt.unit}",
                    _type=vehicle_type,
                    position=pos,
                    group_size=tgt.count,
                )
                for unit in vg.units:
                    unit.skill = skill
                if tgt.late_activation:
                    vg.late_activation = True
                apply_target_motion(
                    vg,
                    airport_position=airport.position,
                    area_center=aoi,
                    tgt=tgt,
                    domain="land",
                    seed=motion_seed_for_spec(spec),
                    target_index=i,
                )
                group_ids.append(vg.id)
        return group_ids

    def _apply_escort(
        self,
        mission,
        countries_mod,
        registry,
        group,
        airport,
        spec: MissionSpec,
        package_types,
        enemy_types,
    ) -> list[int]:
        from dcs.task import CAS, Escort, EscortTaskAction, OptROE

        assert spec.escort is not None
        escort = spec.escort
        destination = airport.position.point_from_heading(
            escort.bearing_deg, escort.distance_km * 1000.0
        )
        package_start = airport.position.point_from_heading(
            escort.bearing_deg, _ESCORT_PACKAGE_START_M
        )

        # Place package first so EscortTaskAction can reference its group id.
        primary_package = None
        for i, (flight, aircraft_type) in enumerate(zip(spec.package, package_types, strict=True)):
            country = self._ensure_country(
                mission, countries_mod, flight.country, flight.coalition.value
            )
            try:
                radio_mhz = registry.radio_mhz(flight.aircraft)
            except RegistryError as exc:
                raise ValueError(str(exc)) from exc

            start = package_start.point_from_heading(90.0 + i * 15.0, 400.0 * (i + 1))
            pkg = mission.flight_group_inflight(
                country=country,
                name=f"Package {flight.aircraft}",
                aircraft_type=aircraft_type,
                position=start,
                altitude=escort.altitude_m,
                speed=_ESCORT_SPEED_KMH,
                group_size=flight.count,
            )
            skill = _skill_from_name(flight.skill)
            for unit in pkg.units:
                unit.skill = skill
            pkg.frequency = radio_mhz
            # Mosquito / fighter-bomber package transit — CAS main task is ME-standard.
            pkg.task = CAS.name
            pkg.add_waypoint(
                destination,
                altitude=escort.altitude_m,
                speed=_ESCORT_SPEED_KMH,
                name="Package destination",
            )
            if primary_package is None:
                primary_package = pkg

        assert primary_package is not None
        group.task = Escort.name
        group.add_waypoint(
            airport.position.point_from_heading(escort.bearing_deg, 5000.0),
            altitude=min(escort.altitude_m, 1500.0),
            speed=_ESCORT_SPEED_KMH,
            name="Climb",
        )
        escort_wp = group.add_waypoint(
            package_start,
            altitude=escort.altitude_m,
            speed=_ESCORT_SPEED_KMH,
            name="Escort",
        )
        escort_wp.add_task(EscortTaskAction(group_id=primary_package.id))
        escort_wp.add_task(OptROE(_opt_roe_value(escort.engagement)))
        group.add_waypoint(
            destination,
            altitude=escort.altitude_m,
            speed=_ESCORT_SPEED_KMH,
            name="Cover",
        )

        if spec.enemies:
            return self._place_escort_enemies(
                mission, countries_mod, registry, spec, enemy_types, destination, escort.altitude_m
            )
        return []

    def _place_escort_enemies(
        self,
        mission,
        countries_mod,
        registry,
        spec: MissionSpec,
        enemy_types,
        destination,
        altitude_m: float,
    ) -> list[int]:
        from dcs.mapping import Point

        enemy_pos = Point(
            destination.x + _ESCORT_BOUNCE_OFFSET_M_X,
            destination.y + _ESCORT_BOUNCE_OFFSET_M_Y,
            mission.terrain,
        )
        altitude = max(altitude_m - 500.0, 500.0)

        group_ids: list[int] = []
        for enemy, aircraft_type in zip(spec.enemies, enemy_types, strict=True):
            country = self._ensure_country(
                mission, countries_mod, enemy.country, enemy.coalition.value
            )
            try:
                radio_mhz = registry.radio_mhz(enemy.aircraft)
            except RegistryError as exc:
                raise ValueError(str(exc)) from exc

            eg = mission.flight_group_inflight(
                country=country,
                name=f"Enemy {enemy.aircraft}",
                aircraft_type=aircraft_type,
                position=enemy_pos,
                altitude=altitude,
                speed=_ENEMY_SPEED_KMH,
                group_size=enemy.count,
            )
            skill = _skill_from_name(enemy.skill)
            for unit in eg.units:
                unit.skill = skill
            eg.frequency = radio_mhz
            if enemy.late_activation:
                eg.late_activation = True
            group_ids.append(eg.id)
        return group_ids

    def _place_enemies(
        self, mission, countries_mod, registry, spec: MissionSpec, enemy_types
    ) -> list[int]:
        from dcs.mapping import Point

        group_ids: list[int] = []
        for enemy, aircraft_type in zip(spec.enemies, enemy_types, strict=True):
            country = self._ensure_country(
                mission, countries_mod, enemy.country, enemy.coalition.value
            )
            try:
                radio_mhz = registry.radio_mhz(enemy.aircraft)
            except RegistryError as exc:
                raise ValueError(str(exc)) from exc

            position = Point(
                _HAWKINGE_X + _DOVER_APPROACH_OFFSET_X,
                _HAWKINGE_Y + _DOVER_APPROACH_OFFSET_Y,
                mission.terrain,
            )
            eg = mission.flight_group_inflight(
                country=country,
                name=f"Enemy {enemy.aircraft}",
                aircraft_type=aircraft_type,
                position=position,
                altitude=_ENEMY_ALTITUDE_M,
                speed=_ENEMY_SPEED_KMH,
                group_size=enemy.count,
            )
            skill = _skill_from_name(enemy.skill)
            for unit in eg.units:
                unit.skill = skill
            eg.frequency = radio_mhz
            if enemy.late_activation:
                eg.late_activation = True
            group_ids.append(eg.id)
        return group_ids

    def _place_cap_enemies(
        self,
        mission,
        countries_mod,
        registry,
        spec: MissionSpec,
        enemy_types,
        airport,
    ) -> list[int]:
        from dcs.mapping import Point

        assert spec.cap is not None
        station = airport.position.point_from_heading(
            spec.cap.bearing_deg, spec.cap.distance_km * 1000.0
        )
        # Offset in metres from station toward a neighbouring patch of sky.
        # Heading offset keeps enemies near the CAP orbit without sharing
        # the intercept Hawkinge corridor unless the station happens to land there.
        enemy_pos = Point(
            station.x + _CAP_ENEMY_OFFSET_M_X,
            station.y + _CAP_ENEMY_OFFSET_M_Y,
            mission.terrain,
        )
        altitude = max(spec.cap.altitude_m - 500.0, 500.0)

        group_ids: list[int] = []
        for enemy, aircraft_type in zip(spec.enemies, enemy_types, strict=True):
            country = self._ensure_country(
                mission, countries_mod, enemy.country, enemy.coalition.value
            )
            try:
                radio_mhz = registry.radio_mhz(enemy.aircraft)
            except RegistryError as exc:
                raise ValueError(str(exc)) from exc

            eg = mission.flight_group_inflight(
                country=country,
                name=f"Enemy {enemy.aircraft}",
                aircraft_type=aircraft_type,
                position=enemy_pos,
                altitude=altitude,
                speed=_ENEMY_SPEED_KMH,
                group_size=enemy.count,
            )
            skill = _skill_from_name(enemy.skill)
            for unit in eg.units:
                unit.skill = skill
            eg.frequency = radio_mhz
            if enemy.late_activation:
                eg.late_activation = True
            group_ids.append(eg.id)
        return group_ids

    @staticmethod
    def _ensure_theatre_member(miz_path: Path, theatre: str) -> None:
        """PyDCS omits the standalone `theatre` member that real .miz files have.

        DCS reads theatre from the mission table too, but we add the file for
        fidelity and to satisfy the compiler acceptance contract.
        """
        import zipfile

        with zipfile.ZipFile(miz_path) as z:
            if "theatre" in z.namelist():
                return
        with zipfile.ZipFile(miz_path, "a", zipfile.ZIP_DEFLATED) as z:
            z.writestr("theatre", theatre)

    def _validate(self, spec: MissionSpec) -> None:
        result = validate_mission_spec(spec, inventory=self._inventory)
        try:
            result.raise_if_errors()
        except MissionValidationError as exc:
            raise ValueError(str(exc)) from exc

    @staticmethod
    def _apply_weather(mission, spec) -> None:
        from ..weather_apply import apply_weather_snapshot
        from ..weather_invent import ensure_weather_seed, resolve_weather_snapshot

        # Always-on invent: deterministic given weather_opts.seed.
        spec = ensure_weather_seed(spec)
        snap = resolve_weather_snapshot(spec)
        apply_weather_snapshot(mission, snap)
