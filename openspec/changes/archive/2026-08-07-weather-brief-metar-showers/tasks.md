## 1. Research reference (local)

- [x] 1.1 Confirm `research/weather.md` R10 section documents upstream
      `CloudPresets` + `DecodePreset` (gitignored; audit only)

## 2. Showers pattern packaging

- [x] 2.1 Add `showers_scattered` to `WeatherPreset` enum
- [x] 2.2 Add YAML recipe + `gallery_family`
      `[RainyPreset4, NEWRAINPRESET4, RainyPreset5, RainyPreset6]` (default
      `RainyPreset4`) in `weather_presets.yaml`
- [x] 2.3 Add planning_options weather entry + catalog sync SoT
- [x] 2.4 Verify `CloudPreset.by_name` accepts family ids (skip/document any
      missing on current PyDCS)

## 3. Synthetic METAR

- [x] 3.1 Package gallery → METAR cloud decode map (Channel data)
- [x] 3.2 Implement `format_synthetic_metar(snap, spec, …)` (offline, seeded,
      `EGMH`, `NOSIG` + `RMK SIM`)
- [x] 3.3 Inject METAR into `build_commander_brief` / weather meteo helper
- [x] 3.4 Confirm compile briefing `l10n` receives the line via shared brief

## 4. Tests and example

- [x] 4.1 Unit tests: invent stays in showers family; METAR deterministic
- [x] 4.2 Weather SoT parity green with `showers_scattered`
- [x] 4.3 Optional example Spec + compile contract (gallery + METAR substring)
- [x] 4.4 ME smoke: open showers `.miz`, confirm light-rain gallery + METAR in
      briefing panel

## 5. Docs

- [x] 5.1 Note in `docs/BACKLOG.md` / lessons if METAR or showers behaviour is
      non-obvious; keep README brief if milestone wording needs a line
