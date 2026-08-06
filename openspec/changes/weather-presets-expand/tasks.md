## 1. Recipes + Spec enum

- [x] 1.1 Extend `weather_presets.yaml` with recipe fields + new pattern ids
- [x] 1.2 Extend `WeatherPreset` enum; registry loads recipe fields
- [x] 1.3 Add planning_options weather rows; keep SoT parity green

## 2. Compiler

- [x] 2.1 Apply `CloudPreset` when recipe has `cloud_preset`; clamp base
- [x] 2.2 Apply wind/fog/temp/QNH/turb from recipe; keep legacy path for density-only
- [x] 2.3 Fail clearly on unknown gallery preset id

## 3. Tests + examples

- [x] 3.1 Hermetic tests: compile asserts gallery preset strings; trio still OK
- [x] 3.2 Example Spec using a new pattern (e.g. broken or rain)
- [x] 3.3 Refresh goldens only if trio emit changes (not needed — trio emit stable)
- [x] 3.4 Optional ME smoke (broken / rain examples) — accepted 2026-08-06 (`manston_broken_channel` / `manston_rain_overcast`)

## 4. Docs / agent

- [x] 4.1 BACKLOG `#17a` → done; README Status one-liner
- [x] 4.2 LESSONS updated (gallery recipes vs legacy density path)
