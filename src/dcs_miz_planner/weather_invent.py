"""Invent-time weather snapshot: season/time priors + always-on seeded jitter."""

from __future__ import annotations

import random
import secrets
import zlib
from dataclasses import dataclass

from .models import MissionSpec, WeatherOpts, WeatherPreset
from .registry import WeatherPresetRef, get_channel_registry


@dataclass(frozen=True)
class WindLayer:
    speed_ms: float
    dir_deg: float


@dataclass(frozen=True)
class WeatherSnapshot:
    """Concrete weather to apply into a mission (compiler / re-weather)."""

    pattern: str
    seed: int
    cloud_preset: str | None
    clouds_density: int | None
    clouds_thickness_m: float | None
    clouds_base_m: float | None
    enable_fog: bool | None
    fog_thickness: float | None
    fog_visibility: float | None
    visibility_distance: float | None
    temperature_c: float | None
    qnh_mmhg: float | None
    turbulence: float | None
    wind_ground: WindLayer | None
    wind_2000: WindLayer | None
    wind_8000: WindLayer | None


def ensure_weather_seed(
    spec: MissionSpec,
    *,
    seed: int | None = None,
    draw: bool = False,
) -> MissionSpec:
    """Return Spec with ``weather_opts.seed`` set.

    - If already set, unchanged.
    - If ``seed`` given, use it.
    - If ``draw`` is True, pick a fresh random seed (persist when writing YAML).
    - Otherwise derive a stable seed from weather + date + start_time so compiles
      without ``weather_opts`` stay reproducible (goldens / ME smoke).
    """
    if spec.weather_opts is not None:
        return spec
    if seed is not None:
        drawn = int(seed)
    elif draw:
        drawn = secrets.randbelow(2_147_483_647)
    else:
        payload = (
            f"{spec.weather.value}|{spec.date.year}-{spec.date.month}-"
            f"{spec.date.day}|{spec.start_time}"
        )
        drawn = zlib.adler32(payload.encode("utf-8")) & 0x7FFFFFFF
    return spec.model_copy(update={"weather_opts": WeatherOpts(seed=drawn)})


def resolve_weather_snapshot(spec: MissionSpec) -> WeatherSnapshot:
    """Resolve deterministic snapshot from Spec weather + date/time + seed."""
    spec = ensure_weather_seed(spec)
    assert spec.weather_opts is not None
    seed = spec.weather_opts.seed
    rng = random.Random(seed)
    ref = get_channel_registry().weather_preset(spec.weather.value)
    month = spec.date.month
    hour = int(spec.start_time.split(":")[0])

    cloud_preset = _pick_gallery(rng, ref, month)
    base = ref.clouds_base_m
    # Soft nudge + jitter (always-on). Legacy density trio: keep recipe base /
    # visibility / density stable for goldens; still nudge fog/temp when present.
    gallery = cloud_preset is not None

    if ref.temperature_c is not None:
        temp = _season_temp(ref.temperature_c, month, hour)
    elif gallery:
        temp = _season_temp(None, month, hour)
    else:
        temp = None
    qnh = ref.qnh_mmhg
    turb = ref.turbulence
    fog_on = ref.enable_fog
    fog_th = ref.fog_thickness
    fog_vis = ref.fog_visibility
    vis = ref.visibility_distance

    if temp is not None:
        temp = temp + rng.uniform(-2.0, 2.0) + _morning_cool(hour)
    if qnh is not None:
        qnh = qnh + rng.uniform(-3.0, 3.0)
    if turb is not None:
        turb = max(0.0, turb + rng.uniform(-3.0, 3.0))
    if gallery and base is not None:
        base = base + rng.uniform(-200.0, 200.0)
    if fog_th is not None and fog_th > 0:
        fog_th = max(0.0, fog_th * rng.uniform(0.85, 1.15))
    if fog_vis is not None and fog_on:
        fog_vis = max(500.0, fog_vis * rng.uniform(0.9, 1.1))
    # Morning sea-fog risk: nudge fog on for gallery patterns in late spring mornings.
    if (
        gallery
        and month in (4, 5, 6)
        and 4 <= hour <= 9
        and fog_on is False
        and rng.random() < 0.25
    ):
        fog_on = True
        fog_th = fog_th or 80.0
        fog_vis = fog_vis or 6000.0

    wind_g = _wind_layer(
        rng,
        ref.wind_ground_speed_ms,
        ref.wind_ground_dir_deg,
        season_boost=_winter_wind_boost(month),
    )
    wind_2 = None
    wind_8 = None
    if wind_g is not None:
        # Aloft: slightly stronger, direction sheared.
        wind_2 = WindLayer(
            speed_ms=max(0.0, wind_g.speed_ms * rng.uniform(1.1, 1.4) + rng.uniform(-0.5, 0.5)),
            dir_deg=(wind_g.dir_deg + rng.uniform(-25.0, 25.0)) % 360.0,
        )
        wind_8 = WindLayer(
            speed_ms=max(0.0, wind_g.speed_ms * rng.uniform(1.3, 1.8) + rng.uniform(-0.5, 1.0)),
            dir_deg=(wind_g.dir_deg + rng.uniform(-40.0, 40.0)) % 360.0,
        )

    return WeatherSnapshot(
        pattern=spec.weather.value,
        seed=seed,
        cloud_preset=cloud_preset,
        clouds_density=ref.clouds_density,
        clouds_thickness_m=ref.clouds_thickness_m,
        clouds_base_m=base,
        enable_fog=fog_on,
        fog_thickness=fog_th,
        fog_visibility=fog_vis,
        visibility_distance=vis,
        temperature_c=temp,
        qnh_mmhg=qnh,
        turbulence=turb,
        wind_ground=wind_g,
        wind_2000=wind_2,
        wind_8000=wind_8,
    )


def _pick_gallery(rng: random.Random, ref: WeatherPresetRef, month: int) -> str | None:
    family = list(ref.gallery_family) if ref.gallery_family else []
    if ref.cloud_preset and ref.cloud_preset not in family:
        family = [ref.cloud_preset, *family]
    if not family:
        return None
    if len(family) == 1:
        return family[0]
    # Season weights: winter → earlier (often lower/wetter in our lists), summer → later.
    weights = []
    for i, _pid in enumerate(family):
        t = i / max(1, len(family) - 1)
        if month in (12, 1, 2):
            w = 1.4 - 0.8 * t
        elif month in (6, 7, 8):
            w = 0.6 + 0.9 * t
        else:
            w = 1.0
        weights.append(max(0.15, w))
    return rng.choices(family, weights=weights, k=1)[0]


def _season_temp(center: float | None, month: int, hour: int) -> float | None:
    if center is None:
        # Legacy trio: invent a Channel-ish temp from month when recipe omits it.
        seasonal = {
            1: 6.0,
            2: 6.0,
            3: 8.0,
            4: 10.0,
            5: 13.0,
            6: 16.0,
            7: 18.0,
            8: 18.0,
            9: 15.0,
            10: 12.0,
            11: 9.0,
            12: 7.0,
        }[month]
        return seasonal + _morning_cool(hour)
    # Nudge recipe center toward seasonal prior (soft).
    seasonal = {
        1: 6.0,
        2: 6.5,
        3: 8.5,
        4: 11.0,
        5: 14.0,
        6: 16.5,
        7: 18.0,
        8: 18.0,
        9: 15.5,
        10: 12.0,
        11: 9.0,
        12: 7.0,
    }[month]
    return 0.7 * center + 0.3 * seasonal


def _morning_cool(hour: int) -> float:
    if 4 <= hour <= 8:
        return -1.0
    if 14 <= hour <= 17:
        return 0.5
    return 0.0


def _winter_wind_boost(month: int) -> float:
    return 1.5 if month in (11, 12, 1, 2, 3) else 0.0


def _wind_layer(
    rng: random.Random,
    speed: float | None,
    direction: float | None,
    *,
    season_boost: float,
) -> WindLayer | None:
    if speed is None and direction is None:
        return None
    spd = float(speed or 0.0) + season_boost * 0.3 + rng.uniform(-1.5, 1.5)
    spd = max(0.0, spd)
    direc = (float(direction or 0.0) + rng.uniform(-30.0, 30.0)) % 360.0
    return WindLayer(speed_ms=spd, dir_deg=direc)


def snapshot_differs(a: WeatherSnapshot, b: WeatherSnapshot) -> bool:
    """True if gallery or key numerics differ (for tests)."""
    if a.cloud_preset != b.cloud_preset:
        return True
    for attr in (
        "clouds_base_m",
        "temperature_c",
        "qnh_mmhg",
        "turbulence",
        "fog_thickness",
        "fog_visibility",
    ):
        va, vb = getattr(a, attr), getattr(b, attr)
        if va is None and vb is None:
            continue
        if va is None or vb is None:
            return True
        if abs(float(va) - float(vb)) > 1e-6:
            return True
    if a.wind_ground is None and b.wind_ground is None:
        return False
    if a.wind_ground is None or b.wind_ground is None:
        return True
    return (
        abs(a.wind_ground.speed_ms - b.wind_ground.speed_ms) > 1e-6
        or abs(a.wind_ground.dir_deg - b.wind_ground.dir_deg) > 1e-6
    )


# Re-export for type checkers / callers.
__all__ = [
    "WeatherPreset",
    "WeatherSnapshot",
    "WindLayer",
    "ensure_weather_seed",
    "resolve_weather_snapshot",
    "snapshot_differs",
]
