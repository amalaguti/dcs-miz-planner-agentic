---
name: dcs-dev-weather
description: >-
  Channel weather presets, invent jitter, fog dynamics, and re-weather pitfalls.
  Use when changing weather Spec enums, weather_invent, fog_dynamics, reweather,
  weather_sot, or debugging .miz meteo / golden weather divergence.
---

# Weather & fog

## Read first

[`docs/lessons/weather.md`](../../../docs/lessons/weather.md)

## Hard rules

1. **Static weather** from Spec `weather` (+ invent jitter) → `.miz` weather table.
2. **Mid-sortie:** only **fog** animation is productizable (`fog_dynamics` →
   curated `setFogAnimation` DoScriptFile). No sunny→rainy / cloud swaps in flight.
3. **Demo fog burn-off** with `sea_fog` start, not `dawn_clear` haze; watch low/ramp.
4. **Invent jitter** must not break goldens on legacy density trio — skip cloud-base
   jitter without gallery; stable derived seed when `weather_opts` omitted at compile;
   `draw=True` only when writing Spec YAML for persisted seed.
5. Keep **weather_sot** / planning_options / registry presets in parity.
6. **Rainy light gallery** (`RainyPreset4`–`6` / `NEWRAINPRESET4`) is not in PyDCS
   `CloudPreset.by_name` — use `weather_gallery.resolve_cloud_preset` (construct from
   packaged min/max). Never invent live METAR; briefs use offline
   `format_synthetic_metar` + `RMK SIM`.

## Code touchpoints

`weather_invent.py`, `weather_apply.py`, `weather_gallery.py`, `weather_metar.py`,
`weather_sot.py`, `fog_dynamics.py`, `compiler/fog_emit.py`, `registry` weather presets,
`reweather.py`, `agent/voice.py`.
