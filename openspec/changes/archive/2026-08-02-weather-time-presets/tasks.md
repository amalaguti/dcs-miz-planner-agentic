## 1. Registry and Spec

- [x] 1.1 Add `dawn_clear` and `marginal_vfr` to `weather_presets.yaml` +
      `models.WeatherPreset` + `planning_options.yaml` (`supported`)
- [x] 1.2 Tests: registry lists presets; validation accepts new ids / rejects unknown;
      `list_mission_options` shows supported weather

## 2. Compiler

- [x] 2.1 Implement `_apply_weather` branches for `dawn_clear` and `marginal_vfr`
      (Preceptions enum; distinct from sunny)
- [x] 2.2 Compile tests asserting weather field differences vs sunny free flight

## 3. Examples and goldens

- [x] 3.1 Add `examples/manston_dawn_freeflight.yaml` and
      `examples/manston_marginal_vfr.yaml` (free flight; dawn ~06:00 / marginal daytime)
- [x] 3.2 Golden or contract coverage for dawn and/or marginal; refresh helpers as needed
  - Contract asserts in `tests/test_weather_presets.py` (visibility/fog/density vs sunny)

## 4. Docs and accept

- [x] 4.1 Update README / ARCHITECTURE / BACKLOG; LESSONS with final weather numbers
- [x] 4.2 In-game accept: sunny (existing), dawn, and marginal VFR `.miz` look correct in
      ME / Instant Action; note in tasks
  - Accepted 2026-08-02: dawn + marginal briefs use meteo descriptions (not Spec ids);
    weather conditions read well in DCS briefing panel
