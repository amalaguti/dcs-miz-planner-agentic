"""Re-weather an existing .miz (overwrite) via Spec recompile or weather-table patch."""

from __future__ import annotations

from pathlib import Path

from .compiler import PyDCSCompiler
from .loader import SpecLoadError, load_mission_spec
from .models import MissionDate, MissionSpec, Player, WeatherOpts, WeatherPreset
from .weather_apply import apply_weather_snapshot
from .weather_invent import ensure_weather_seed, resolve_weather_snapshot


class ReweatherError(ValueError):
    """Raised when re-weather cannot complete."""


def find_spec_sidecar(miz_path: Path) -> Path | None:
    """Return sibling Spec YAML for a `.miz` if present."""
    for suffix in (".yaml", ".yml"):
        candidate = miz_path.with_suffix(suffix)
        if candidate.is_file():
            return candidate
    return None


def reweather_mission(
    miz_path: str | Path,
    weather: str | WeatherPreset,
    *,
    seed: int | None = None,
    spec_path: str | Path | None = None,
    voice: str | None = None,
    inventory=None,
) -> dict:
    """Change weather on an existing mission and overwrite the `.miz`.

    Prefers Spec sidecar (or explicit ``spec_path``) → update weather/seed →
    recompile. Otherwise loads the `.miz`, applies invent snapshot, saves.
    """
    miz = Path(miz_path)
    if not miz.is_file():
        raise ReweatherError(f"Mission not found: {miz}")

    try:
        preset = weather if isinstance(weather, WeatherPreset) else WeatherPreset(weather)
    except ValueError as exc:
        known = ", ".join(p.value for p in WeatherPreset)
        raise ReweatherError(f"Unknown weather {weather!r}. Known: {known}") from exc

    spec_file = Path(spec_path) if spec_path is not None else find_spec_sidecar(miz)
    if spec_file is not None:
        return _reweather_via_spec(
            miz, spec_file, preset, seed=seed, voice=voice, inventory=inventory
        )
    return _reweather_via_miz_patch(miz, preset, seed=seed)


def _miz_theatre_id(miz: Path) -> str | None:
    import zipfile

    try:
        with zipfile.ZipFile(miz) as z:
            if "theatre" not in z.namelist():
                return None
            return z.read("theatre").decode("utf-8").strip() or None
    except (OSError, zipfile.BadZipFile):
        return None


def _reweather_via_spec(
    miz: Path,
    spec_file: Path,
    preset: WeatherPreset,
    *,
    seed: int | None,
    voice: str | None,
    inventory,
) -> dict:
    from .agent.planner import write_spec_yaml

    if not spec_file.is_file():
        raise ReweatherError(f"Spec not found: {spec_file}")
    try:
        spec = load_mission_spec(spec_file)
    except SpecLoadError as exc:
        raise ReweatherError(str(exc)) from exc

    updates: dict = {"weather": preset}
    if seed is not None:
        updates["weather_opts"] = WeatherOpts(seed=int(seed))
    else:
        # New invent day when changing weather (or re-rolling same pattern).
        updates["weather_opts"] = None
    spec = spec.model_copy(update=updates)
    spec = ensure_weather_seed(spec, draw=seed is None, seed=seed)

    write_spec_yaml(spec, spec_file)
    try:
        written = PyDCSCompiler(inventory=inventory).compile(spec, miz, voice=voice)
    except ValueError as exc:
        raise ReweatherError(str(exc)) from exc

    return {
        "ok": True,
        "mode": "spec_recompile",
        "miz_path": str(written),
        "spec_path": str(spec_file),
        "weather": preset.value,
        "seed": spec.weather_opts.seed if spec.weather_opts else None,
        "note": "Reload the mission in ME if it was open during overwrite.",
    }


def _reweather_via_miz_patch(
    miz: Path,
    preset: WeatherPreset,
    *,
    seed: int | None,
) -> dict:
    from dcs.mission import Mission

    from .theatre_terrain import TheatreTerrainError, terrain_for_theatre

    theatre = _miz_theatre_id(miz)
    if theatre != "TheChannel":
        raise ReweatherError(
            "Miz-patch reweather is only supported for theatre TheChannel "
            f"(got {theatre!r}). Provide a Spec sidecar to recompile."
        )

    try:
        terrain = terrain_for_theatre("TheChannel")
    except TheatreTerrainError as exc:
        raise ReweatherError(str(exc)) from exc

    mission = Mission(terrain=terrain)
    try:
        mission.load_file(str(miz))
    except Exception as exc:
        raise ReweatherError(f"Failed to load mission {miz}: {exc}") from exc

    start = mission.start_time
    date = MissionDate(year=start.year, month=start.month, day=start.day)
    start_time = f"{start.hour:02d}:{start.minute:02d}"
    spec = MissionSpec(
        schema_version="1",
        theatre="TheChannel",
        date=date,
        start_time=start_time,
        weather=preset,
        player=Player(aircraft="SpitfireLFMkIX", airfield="Manston"),
    )
    if seed is not None:
        spec = ensure_weather_seed(spec, seed=seed)
    else:
        spec = ensure_weather_seed(spec, draw=True)

    snap = resolve_weather_snapshot(spec)
    apply_weather_snapshot(mission, snap)
    try:
        mission.save(str(miz))
    except Exception as exc:
        raise ReweatherError(f"Failed to save mission {miz}: {exc}") from exc

    return {
        "ok": True,
        "mode": "miz_patch",
        "miz_path": str(miz),
        "spec_path": None,
        "weather": preset.value,
        "seed": snap.seed,
        "note": "Reload the mission in ME if it was open during overwrite.",
    }
