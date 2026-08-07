# Weather & fog

Detailed lessons for this topic. Newest first within this file.
Index: [`../LESSONS_LEARNED.md`](../LESSONS_LEARNED.md).

---

## Synthetic METAR + rainy light gallery beyond PyDCS (2026-08-07)

- **Date:** 2026-08-07
- **Lesson:** Briefs can emit a deterministic ICAO-style METAR from invent
  `WeatherSnapshot` (`weather_metar.format_synthetic_metar`) without live APIs —
  always mark `NOSIG RMK SIM` and use a fixed Channel station (`EGMH`). Separately,
  PyDCS `CloudPreset.by_name` (0.15.x) only knows `Preset1`–`27` + `RainyPreset1`–`3`.
  DCS ME still accepts rainy light ids (`RainyPreset4`–`6`, `NEWRAINPRESET4`) used by
  dcs-real-weather. For `showers_scattered`, package min/max + METAR decode in
  `weather_gallery.yaml` and construct a `CloudPreset` when `by_name` fails so
  `_make_cloud_dict` writes the gallery string. Do not silently fold light-rain into
  `rain_overcast` (`RainyPreset1`–`3`).
- **Code:** `weather_metar.py`, `weather_gallery.py`, `weather_apply.resolve_cloud_preset`,
  `agent/voice.py`, `data/channel/weather_gallery.yaml`.

## In-flight weather: fog yes, clouds/rain no (2026-08-06)

- **Date:** 2026-08-06
- **Lesson:** DCS mission scripting `world.weather` (2.9.10+) can animate **fog**
  thickness/visibility mid-sortie (`setFogAnimation`). It cannot change cloud
  presets, precip, or wind while the mission is running — those are fixed in the
  `.miz` weather table. Invent-time randomness among campaign-seeded patterns is
  fine (`#17a` + `#17e` invent jitter); sunny→rainy *during* flight is not
  productizable without ED APIs. Foggy↔clear belongs in `#17c` + curated
  snippets, never LLM Lua. `#17c` ships a fog-only slice: Spec `fog_dynamics` →
  PyDCS `DoScriptFile` + `l10n/DEFAULT/fog_dynamics.lua` with human template
  `world.weather.setFogAnimation({{duration}, vis, thick})` on ONCE `TimeAfter`.
  **Do not** use `DoScript(mission.string(lua))` for this: ME shows
  `DictKey_Translation_N`, and if the dict value is empty/missing DCS executes
  the key name → ` '=' expected near '<eof>'` (pydcs#179). Prefer
  `DoScriptFile` / map resources for curated snippets.
  Starting weather matters: `dawn_clear` is only ~8 km / 80 m haze — burn-off
  looks invisible. Use `sea_fog` (~1 km / 400 m) for ME demos; watch from the
  ramp or stay low (above the layer the change is easy to miss).
- **Code / notes:** `fog_dynamics.py`, `compiler/fog_emit.py`; ED FAQ weather
  singleton; backlog `#17c` / `#22`.

## Weather invent seed vs golden stability (2026-08-06)

- **Date:** 2026-08-06
- **Lesson:** Always-on invent jitter (`weather_invent.resolve_weather_snapshot`)
  must not break structural goldens on the legacy density trio. Skip cloud-base
  jitter (and inventing temperature) when there is no gallery preset; use a
  **stable derived seed** from weather+date+time when `weather_opts` is omitted
  at compile; use `draw=True` only when writing Spec YAML so sidecars get a
  persisted random seed. Pin explicit seeds in invent hermetic tests.
- **Code:** `weather_invent.py`, `write_spec_yaml`, `_apply_weather`.

## PyDCS cloud presets vs legacy density weather (2026-08-06)

- **Date:** 2026-08-06
- **Lesson:** Modern ME static weather uses a **cloud preset gallery**
  (`clouds.preset` = `PresetN` / `RainyPresetN`). PyDCS exposes this as
  `Weather.clouds_preset = CloudPreset.by_name(...)` via `dcs.cloud_presets`
  (30 presets in 0.15.x; each has min/max `clouds_base` metres — validate or
  clamp). `#17a` recipes set `cloud_preset` + numerics for expanded Spec ids;
  the original trio (`sunny_clear` / `dawn_clear` / `marginal_vfr`) keeps the
  legacy density/thickness path (`clouds_preset = None`). Clamp base into
  gallery min/max. Campaign rainy gallery often leaves `iprecptns=0` — rain look
  from the preset, not the precip enum. **Best reference corpus:** installed
  Spitfire campaign `.miz` weather tables (Beware / Fight or Die / Epsom / Big
  Show) — not empty ME weather-template folders. Mission `weather.name` is often
  a stale `"Winter, clean sky"` string; trust `clouds.preset` + numerics.
- **Code:** `compiler/pydcs_compiler._apply_weather`, `weather_presets.yaml`,
  `dcs.cloud_presets`, research notes in gitignored `research/weather.md`.

## Weather SoT parity (2026-08-05)

- **Date:** 2026-08-05
- **Lesson:** Weather ids must stay equal across `WeatherPreset` enum,
  `weather_presets.yaml`, planning_options `weather` family, and
  `PyDCSCompiler._apply_weather` branches. Use `weather_sot.collect_weather_sot()` /
  `test_weather_sot_parity` when adding a preset — do not update only one surface.
- **Code:** `weather_sot.py`, `tests/test_weather_presets.py`.

## Mission randomization: seed is build-scoped, not forever-stable

- **Date:** 2026-08-02
- **Lesson:** `randomize_mission_spec` uses `random.Random(seed)` with a fixed draw order
  (weather → time → geometry → opposition). Same seed is reproducible **only for the
  current axis set and choice pools**. Adding WeatherPreset values, opposition fighters,
  new default axes, or changing jitter math will change Specs for old seeds. Lock a
  sortie by keeping the randomized YAML / `.miz`, not the seed alone. Never put RNG in
  the compiler — goldens stay on concrete Specs.
- **Code:** `randomize.py`, `dcs-miz randomize`, tools `randomize_mission`.

## Weather presets: dawn_clear / marginal_vfr mappings

- **Date:** 2026-08-02
- **Lesson:** Beyond `sunny_clear` (80 km, no fog): `dawn_clear` uses density 1, light fog
  (`enable_fog`, thickness 80, fog_visibility 8000) and visibility 45 km — pair with
  `start_time` ~06:00. `marginal_vfr` uses density 8, base 700, thickness 1500, visibility
  6000 m, no fog. Always set `clouds_iprecptns` via `Weather.Preceptions` enum. Catalog
  schema bumped to 3 so `ensure_synced` rebuilds planning options after YAML adds.
  Commander briefs and `.miz` l10n MUST use registry weather **descriptions** (meteo
  English), never raw Spec ids like `marginal_vfr`.
- **Code:** `compiler/pydcs_compiler.py` (`_apply_weather`), `weather_presets.yaml`,
  `agent/voice.py` (`_weather_phrase`), `examples/manston_dawn_freeflight.yaml`,
  `examples/manston_marginal_vfr.yaml`.
