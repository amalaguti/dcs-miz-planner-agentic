## 1. Spec + registry

- [x] 1.1 Add optional `WeatherOpts` / `weather_opts.seed` on Mission Spec
- [x] 1.2 Extend weather YAML/registry with `gallery_family` lists per gallery pattern
- [x] 1.3 BACKLOG `#17e` → building; README Status one-liner

## 2. Invent module

- [x] 2.1 Implement `resolve_weather_snapshot` (season/time weights, within-family pick, nudge, jitter)
- [x] 2.2 Seed draw + helper to persist `weather_opts.seed` when writing Spec YAML
- [x] 2.3 Wind layers on snapshot (ground + aloft heuristics)

## 3. Compiler

- [x] 3.1 Apply invent snapshot in `_apply_weather` (clamp gallery base; multi-layer wind)
- [x] 3.2 Ensure compile path ensures seed when Spec output path available

## 4. Tests + examples

- [x] 4.1 Hermetic tests: same seed stable; different seeds differ; rain stays rainy family; sunny no rain gallery
- [x] 4.2 Pin `weather_opts.seed` on examples/goldens that need stable emit
- [x] 4.3 Optional ME smoke: two seeds same pattern, confirm weather differs in ME — accepted 2026-08-06 (Broken 5 vs 6; fog/other differ; look differs)

## 5. Docs

- [x] 5.1 LESSONS if invent/clamp pitfalls appear
