## 1. Shared apply + library

- [x] 1.1 Extract `apply_weather_snapshot` for compiler + re-weather
- [x] 1.2 Implement `reweather_mission` (sidecar discover, Spec recompile, miz patch)
- [x] 1.3 New seed by default; optional explicit seed

## 2. CLI + agent

- [x] 2.1 CLI subcommand to re-weather (overwrite)
- [x] 2.2 Agent tool + dispatch; mutating gated like compile
- [x] 2.3 BACKLOG `#17d` building; README one-liner

## 3. Tests

- [x] 3.1 Hermetic: Spec sidecar path updates weather in overwritten `.miz`
- [x] 3.2 Hermetic: miz-only patch changes weather without Spec
- [x] 3.3 Optional ME smoke: re-weather example, open in ME — accepted 2026-08-06 (`rain_overcast` → Overcast and Rain 2)

## 4. Docs

- [x] 4.1 LESSONS if load/save pitfalls appear (none beyond reload note)
