"""Offline synthetic METAR from invent WeatherSnapshot (no live meteo APIs)."""

from __future__ import annotations

from .models import MissionSpec
from .weather_gallery import gallery_preset_meta
from .weather_invent import WeatherSnapshot

# Manston / Channel synthetic station (not a live observation).
DEFAULT_ICAO = "EGMH"
_MPS_TO_KT = 1.944
_MMHG_TO_INHG = 1.0 / 25.4
_METERS_TO_SM = 3.28084 / 5280.0


def format_synthetic_metar(
    snap: WeatherSnapshot,
    spec: MissionSpec,
    *,
    icao: str = DEFAULT_ICAO,
) -> str:
    """Build one ICAO-style METAR line from snapshot + Spec date/time.

    Deterministic for the same inputs. Always ends with ``NOSIG RMK SIM``.
    """
    parts: list[str] = [icao.strip().upper() or DEFAULT_ICAO]
    parts.append(_obs_time_group(spec))
    parts.append(_wind_group(snap))
    parts.append(_vis_group(snap))
    precip = _precip_group(snap)
    if precip:
        parts.append(precip)
    parts.append(_clouds_group(snap))
    parts.append(_temp_dew_group(snap))
    parts.append(_altimeter_group(snap))
    parts.append("NOSIG")
    parts.append("RMK SIM")
    return " ".join(parts)


def _obs_time_group(spec: MissionSpec) -> str:
    hour_s, minute_s, *_ = (spec.start_time.split(":") + ["0", "0"])[:3]
    hour = int(hour_s)
    minute = int(minute_s)
    return f"{spec.date.day:02d}{hour:02d}{minute:02d}Z"


def _wind_group(snap: WeatherSnapshot) -> str:
    if snap.wind_ground is None:
        return "00000KT"
    speed_kt = int(snap.wind_ground.speed_ms * _MPS_TO_KT + 0.5)
    direction = int(snap.wind_ground.dir_deg) % 360
    if speed_kt <= 0:
        return "00000KT"
    if direction == 0:
        direction = 360
    return f"{direction:03d}{speed_kt:02d}KT"


def _vis_group(snap: WeatherSnapshot) -> str:
    meters = snap.visibility_distance
    if meters is None:
        return "10SM"
    if snap.enable_fog and snap.fog_visibility is not None:
        meters = min(meters, snap.fog_visibility)
    sm = meters * _METERS_TO_SM
    if sm > 10:
        return "10SM"
    if sm <= 0.25:
        return "1/4SM"
    if sm <= 0.5:
        return "1/2SM"
    if sm <= 0.75:
        return "3/4SM"
    return f"{int(sm + 0.5)}SM"


def _precip_group(snap: WeatherSnapshot) -> str | None:
    if not snap.cloud_preset:
        return None
    meta = gallery_preset_meta(snap.cloud_preset)
    return meta.precip if meta is not None else None


def _clouds_group(snap: WeatherSnapshot) -> str:
    if not snap.cloud_preset:
        return "CLR"
    meta = gallery_preset_meta(snap.cloud_preset)
    if meta is None or not meta.metar_layers:
        return "CLR"
    base_m = snap.clouds_base_m
    chunks: list[str] = []
    for i, layer in enumerate(meta.metar_layers):
        if i == 0 and base_m is not None:
            # Hundreds of feet AGL from invent base (metres).
            hundreds = int(float(base_m) * 3.28084 + 50) // 100
            hundreds = max(0, min(999, hundreds))
            chunks.append(f"{layer.code}{hundreds:03d}")
        else:
            chunks.append(f"{layer.code}{layer.base_100ft}")
    return " ".join(chunks)


def _temp_dew_group(snap: WeatherSnapshot) -> str:
    temp_f = float(snap.temperature_c) if snap.temperature_c is not None else 15.0
    temp: int = round(temp_f)
    dew = _dewpoint_c(temp, snap)
    return f"{_temp_token(temp)}/{_temp_token(dew)}"


def _dewpoint_c(temp_c: int, snap: WeatherSnapshot) -> int:
    """Approximate dewpoint from temp + fog/vis cues (not a psychrometer)."""
    if snap.enable_fog and snap.fog_visibility is not None and snap.fog_visibility < 3000:
        dew = temp_c - 1
    elif snap.visibility_distance is not None and snap.visibility_distance < 8000:
        dew = temp_c - 2
    else:
        dew = temp_c - 4
    return min(dew, temp_c)


def _temp_token(celsius: int) -> str:
    if celsius < 0:
        return f"M{abs(celsius):02d}"
    return f"{celsius:02d}"


def _altimeter_group(snap: WeatherSnapshot) -> str:
    mmhg = snap.qnh_mmhg if snap.qnh_mmhg is not None else 760.0
    inhg = mmhg * _MMHG_TO_INHG
    return f"A{int(inhg * 100 + 0.5):04d}"


__all__ = ["DEFAULT_ICAO", "format_synthetic_metar"]
