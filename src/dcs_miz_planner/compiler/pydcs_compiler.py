"""PyDCS-backed compiler for free-flight missions.

Boundary rule: this module is the only place allowed to import PyDCS.
The rest of the app depends on `MissionSpec` and `CompilerInterface`.
"""

from __future__ import annotations

import datetime
from pathlib import Path

from ..models import MissionSpec, StartType, WeatherPreset
from ..reference import (
    KNOWN_AIRCRAFT,
    SUPPORTED_THEATRES,
    airdrome_id,
    radio_frequency_mhz,
)
from .base import CompilerInterface


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


class PyDCSCompiler(CompilerInterface):
    """Compile a free-flight Mission Spec into a .miz via PyDCS."""

    def compile(self, spec: MissionSpec, output_path: str | Path) -> Path:
        # Imports are local so the boundary is explicit and importing our
        # package never eagerly pulls PyDCS.
        from dcs import countries
        from dcs.mission import Mission
        from dcs.mission import StartType as DcsStartType
        from dcs.planes import plane_map
        from dcs.terrain import TheChannel
        from dcs.unit import Skill

        self._validate(spec)

        aircraft_type = plane_map.get(spec.player.aircraft)
        if aircraft_type is None:
            raise ValueError(f"Unknown PyDCS plane id: {spec.player.aircraft}")

        _disable_payload_scan(aircraft_type)

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

        country = mission.country(spec.player.country)
        if country is None:
            country_cls = getattr(countries, spec.player.country, None)
            if country_cls is None:
                raise ValueError(f"Unknown country: {spec.player.country}")
            mission.coalition[spec.player.coalition.value].add_country(country_cls())
            country = mission.country(spec.player.country)

        airport = mission.terrain.airport_by_id(airdrome_id(spec.theatre, spec.player.airfield))
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
        group.units[0].skill = Skill.Player

        # PyDCS defaults groups to 251 MHz, outside the WWII VHF bands; DCS
        # refuses the flight with a radio warning. Assigning the group
        # frequency is enough — DCS tunes the first radio channel from it.
        group.frequency = radio_frequency_mhz(spec.player.aircraft)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        mission.save(str(out))
        self._ensure_theatre_member(out, spec.theatre)
        return out

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

    @staticmethod
    def _validate(spec: MissionSpec) -> None:
        if spec.theatre not in SUPPORTED_THEATRES:
            raise ValueError(
                f"Unsupported theatre '{spec.theatre}'. Supported: {sorted(SUPPORTED_THEATRES)}"
            )
        if spec.player.aircraft not in KNOWN_AIRCRAFT:
            raise ValueError(
                f"Unknown aircraft '{spec.player.aircraft}'. Known: {sorted(KNOWN_AIRCRAFT)}"
            )

    @staticmethod
    def _apply_weather(mission, preset: WeatherPreset) -> None:
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
