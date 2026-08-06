"""Curated mid-sortie fog animation Lua (human-authored templates only)."""

from __future__ import annotations

from .models import FogDynamics, FogDynamicsMode


def build_fog_animation_lua(fog: FogDynamics) -> str:
    """Return DoScript body for ``world.weather.setFogAnimation``."""
    duration = int(fog.duration_s)
    if fog.mode is FogDynamicsMode.BURN_OFF:
        # Clear fog over duration (vis/thick 0 removes fog at that key).
        end_vis = int(fog.end_visibility_m) if fog.end_visibility_m is not None else 0
        end_th = int(fog.end_thickness_m) if fog.end_thickness_m is not None else 0
        return f"world.weather.setFogAnimation({{\n  {{{duration}, {end_vis}, {end_th}}}\n}})\n"
    if fog.mode is FogDynamicsMode.ROLL_IN:
        end_vis = int(fog.end_visibility_m) if fog.end_visibility_m is not None else 3000
        end_th = int(fog.end_thickness_m) if fog.end_thickness_m is not None else 200
        # Clamp to ED documented ranges when non-zero.
        if end_vis > 0:
            end_vis = max(100, min(100_000, end_vis))
        if end_th > 0:
            end_th = max(100, min(5_000, end_th))
        return f"world.weather.setFogAnimation({{\n  {{{duration}, {end_vis}, {end_th}}}\n}})\n"
    raise ValueError(f"Unsupported fog_dynamics mode: {fog.mode!r}")
