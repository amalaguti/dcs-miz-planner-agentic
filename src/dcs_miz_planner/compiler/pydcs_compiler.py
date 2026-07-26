"""PyDCS-backed compiler for free-flight and intercept missions.

Boundary rule: this module is the only place allowed to import PyDCS.
The rest of the app depends on `MissionSpec` and `CompilerInterface`.
"""

from __future__ import annotations

import datetime
from pathlib import Path

from ..install.models import TheatreInventory
from ..models import MissionSpec, MissionType, StartType, WeatherPreset
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


def _disable_payload_scan(*unit_types) -> None:
    """Work around a PyDCS bug when a real DCS install is present.

    ``load_payloads`` indexes ``_payload_cache[path]`` for payload files that
    ``scan_payload_dir`` skipped (files without a ``["unitType"]`` line),
    raising ``KeyError``. Free-flight missions need no payloads, so we mark the
    cache non-empty (skip scanning the install) and give each used type an empty
    payload set (early-return before the buggy loop).
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


class PyDCSCompiler(CompilerInterface):
    """Compile a Mission Spec into a .miz via PyDCS."""

    def __init__(self, *, inventory: TheatreInventory | None = None) -> None:
        # Optional inject for tests; production uses the SQLite install cache.
        self._inventory = inventory

    def compile(self, spec: MissionSpec, output_path: str | Path) -> Path:
        # Imports are local so the boundary is explicit and importing our
        # package never eagerly pulls PyDCS.
        from dcs import countries
        from dcs.mission import Mission
        from dcs.mission import StartType as DcsStartType
        from dcs.planes import plane_map
        from dcs.terrain import TheChannel

        self._validate(spec)

        aircraft_type = plane_map.get(spec.player.aircraft)
        if aircraft_type is None:
            raise ValueError(f"Unknown PyDCS plane id: {spec.player.aircraft}")

        enemy_types = []
        for enemy in spec.enemies:
            et = plane_map.get(enemy.aircraft)
            if et is None:
                raise ValueError(f"Unknown PyDCS plane id: {enemy.aircraft}")
            enemy_types.append(et)

        _disable_payload_scan(aircraft_type, *enemy_types)

        mission = Mission(terrain=TheChannel())

        # Date + time. PyDCS start_time is a datetime; DCS mission time is
        # naive local mission time (no timezone).
        mission.start_time = datetime.datetime(  # noqa: DTZ001
            spec.date.year,
            spec.date.month,
            spec.date.day,
            spec.start_seconds // 3600,
            (spec.start_seconds % 3600) // 60,
        )

        self._apply_weather(mission, spec.weather)

        country = self._ensure_country(
            mission, countries, spec.player.country, spec.player.coalition.value
        )

        registry = get_channel_registry()
        try:
            airport_id = registry.airdrome_id(spec.player.airfield)
            radio_mhz = registry.radio_mhz(spec.player.aircraft)
        except RegistryError as exc:
            raise ValueError(str(exc)) from exc

        airport = mission.terrain.airport_by_id(airport_id)
        if airport is None:
            raise ValueError(f"Airport not found for {spec.player.airfield}")

        start_type_map = {StartType.COLD_PARKING: DcsStartType.Cold}
        start_type = start_type_map[spec.player.start]

        group = mission.flight_group_from_airport(
            country=country,
            name=spec.name,
            aircraft_type=aircraft_type,
            airport=airport,
            start_type=start_type,
            group_size=1,
        )
        group.units[0].skill = _skill_from_name(spec.player.skill)

        # PyDCS defaults groups to 251 MHz, outside the WWII VHF bands; DCS
        # refuses the flight with a radio warning. Assigning the group
        # frequency is enough — DCS tunes the first radio channel from it.
        group.frequency = radio_mhz

        if spec.mission_type is MissionType.INTERCEPT:
            self._place_enemies(mission, countries, registry, spec, enemy_types)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        mission.save(str(out))
        self._ensure_theatre_member(out, spec.theatre)
        return out

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

    def _place_enemies(
        self, mission, countries_mod, registry, spec: MissionSpec, enemy_types
    ) -> None:
        from dcs.mapping import Point

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
    def _apply_weather(mission, preset: WeatherPreset) -> None:
        # Existence already checked in _validate via the Channel registry.
        if preset is WeatherPreset.SUNNY_CLEAR:
            from dcs.weather import Weather

            w = mission.weather
            w.clouds_preset = None
            w.clouds_density = 0
            w.clouds_thickness = 0
            w.clouds_iprecptns = Weather.Preceptions.None_
            w.enable_fog = False
            w.enable_dust = False
            w.dust_density = 0
            w.visibility_distance = 80000
        else:  # pragma: no cover - single preset in v1
            raise ValueError(f"Unsupported weather preset: {preset}")
