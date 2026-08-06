"""Apply invent weather snapshots to a loaded PyDCS Mission."""

from __future__ import annotations

from .weather_invent import WeatherSnapshot


def apply_weather_snapshot(mission, snap: WeatherSnapshot) -> None:
    """Write a resolved invent snapshot into ``mission.weather`` (static)."""
    from dcs.weather import CloudPreset, Weather, Wind

    w = mission.weather
    w.atmosphere_type = 0
    w.enable_dust = False
    w.dust_density = 0
    w.clouds_iprecptns = Weather.Preceptions.None_
    w.clouds_preset = None

    if snap.clouds_density is not None:
        w.clouds_density = snap.clouds_density
    if snap.clouds_thickness_m is not None:
        w.clouds_thickness = round(snap.clouds_thickness_m)
    if snap.clouds_base_m is not None:
        w.clouds_base = round(snap.clouds_base_m)
    if snap.enable_fog is not None:
        w.enable_fog = snap.enable_fog
    if snap.fog_thickness is not None:
        w.fog_thickness = round(snap.fog_thickness)
    if snap.fog_visibility is not None:
        w.fog_visibility = round(snap.fog_visibility)
    if snap.visibility_distance is not None:
        w.visibility_distance = round(snap.visibility_distance)
    if snap.temperature_c is not None:
        w.season_temperature = float(snap.temperature_c)
    if snap.qnh_mmhg is not None:
        w.qnh = float(snap.qnh_mmhg)
    if snap.turbulence is not None:
        turb = float(snap.turbulence)
        w.turbulence_at_ground = int(turb) if turb.is_integer() else turb
    if snap.wind_ground is not None:
        w.wind_at_ground = Wind(
            direction=float(snap.wind_ground.dir_deg),
            speed=float(snap.wind_ground.speed_ms),
        )
    if snap.wind_2000 is not None:
        w.wind_at_2000 = Wind(
            direction=float(snap.wind_2000.dir_deg),
            speed=float(snap.wind_2000.speed_ms),
        )
    if snap.wind_8000 is not None:
        w.wind_at_8000 = Wind(
            direction=float(snap.wind_8000.dir_deg),
            speed=float(snap.wind_8000.speed_ms),
        )

    if snap.cloud_preset:
        try:
            gallery = CloudPreset.by_name(snap.cloud_preset)
        except Exception as exc:
            raise ValueError(
                f"Unknown weather cloud_preset {snap.cloud_preset!r} for {snap.pattern}"
            ) from exc
        w.clouds_preset = gallery
        base = w.clouds_base
        if base < gallery.min_base:
            w.clouds_base = gallery.min_base
        elif base > gallery.max_base:
            w.clouds_base = gallery.max_base
