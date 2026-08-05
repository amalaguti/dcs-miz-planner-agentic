"""Weather preset source-of-truth collectors for parity tests.

Ids only — descriptions may differ across YAML and planning_options.
"""

from __future__ import annotations

import inspect
import re
from dataclasses import dataclass

from .compiler.pydcs_compiler import PyDCSCompiler
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
    """Preset values referenced as ``WeatherPreset.NAME`` in ``_apply_weather``."""
    src = inspect.getsource(PyDCSCompiler._apply_weather)
    names = re.findall(r"WeatherPreset\.([A-Z0-9_]+)", src)
    ids: set[str] = set()
    for name in names:
        try:
            ids.add(WeatherPreset[name].value)
        except KeyError:
            continue
    return frozenset(ids)


def collect_weather_sot() -> WeatherSotSets:
    return WeatherSotSets(
        enum=enum_weather_ids(),
        yaml=yaml_weather_ids(),
        planning=planning_weather_ids(),
        compiler=compiler_weather_ids(),
    )
