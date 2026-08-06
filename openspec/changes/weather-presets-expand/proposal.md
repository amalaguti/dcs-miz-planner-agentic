## Why

Channel missions still only offer three Spec weather ids (`sunny_clear`,
`dawn_clear`, `marginal_vfr`) compiled with legacy density/thickness — while
installed Spitfire campaigns already use the modern ME cloud-preset gallery.
Expanding named Spec patterns (seeded from that corpus) makes invent/`randomize`
and briefs much richer without exposing raw ME knobs or mid-flight cloud swaps.

## What Changes

- Expand `WeatherPreset` / `weather_presets.yaml` / planning_options with curated
  Channel patterns (gallery `CloudPreset` + wind/fog/temp/QNH/turb defaults).
- Compiler applies `Weather.clouds_preset` (clamp base to preset min/max) instead of
  density-only for gallery recipes; keep existing three presets behaviourally
  compatible (or migrate them carefully with golden/example updates).
- Optional invent-time / `randomize` choice among the enlarged set (Layer A jitter
  of numeric knobs can be minimal in this change).
- Catalog/agent see new weather as `supported` with pilot-facing descriptions.
- **Out of scope:** mid-flight sunny→rain (`#17c` fog-only later); live METAR;
  dynamic cyclones; static objects (`#17b`).

## Capabilities

- `mission-spec`: more WeatherPreset enum values / documented weather field.
- `reference-registry` / weather packaging: richer YAML recipe fields.
- `miz-compiler`: CloudPreset emit + wind/fog/turb from recipes.
- `mission-options` / `mission-validation` / agent surfaces: list & validate new ids.
- `mission-randomization`: weather axis picks from expanded set.

## Impact

- Examples may add 1–2 new Specs; goldens that embed weather may need refresh if
  legacy trio emit changes.
- `weather_sot` parity must include new ids across enum/YAML/planning/compiler.
- Briefing voice continues to use registry descriptions.
