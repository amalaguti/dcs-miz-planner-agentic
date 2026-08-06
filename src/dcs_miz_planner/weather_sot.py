"""Weather preset source-of-truth collectors for parity tests.

Ids only — descriptions may differ across YAML and planning_options.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import WeatherPreset
from .registry import get_channel_registry


@dataclass(frozen=True)
class WeatherSotSets:
    enum: frozenset[str]
    yaml: frozenset[str]
    planning: frozenset[str]
    compiler: frozenset[str]

    @property
    def aligned(self) -> bool:
        return self.enum == self.yaml == self.planning == self.compiler


def enum_weather_ids() -> frozenset[str]:
    return frozenset(p.value for p in WeatherPreset)


def yaml_weather_ids() -> frozenset[str]:
    return frozenset(get_channel_registry().list_weather_presets())


def planning_weather_ids() -> frozenset[str]:
    registry = get_channel_registry()
    return frozenset(opt.id for opt in registry.list_planning_options() if opt.family == "weather")


def compiler_weather_ids() -> frozenset[str]:
    """All Spec weather ids are applied via registry recipes in ``_apply_weather``."""
    return enum_weather_ids()


def collect_weather_sot() -> WeatherSotSets:
    return WeatherSotSets(
        enum=enum_weather_ids(),
        yaml=yaml_weather_ids(),
        planning=planning_weather_ids(),
        compiler=compiler_weather_ids(),
    )
