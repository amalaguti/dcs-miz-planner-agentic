## Why

Named Channel weather patterns (`#17a`) are fixed recipes today — every
`broken_channel` sortie looks identical. Real Channel weather varies day to day
within the same class; invent-time variation (seeded, reproducible) makes
missions feel alive without ME Dynamic cyclones or mid-flight cloud swaps.

## What Changes

- Always-on invent variation for Spec weather: within-family gallery pick
  weighted by date/season (+ start time cues), soft numeric nudge
  (temp/QNH/wind layers/turb/fog/base), then seeded jitter
- Optional Spec `weather_opts.seed`; auto-write into YAML when omitted so
  sidecar compiles reproduce
- Shared weather-snapshot apply path (prep for `#17d` re-weather); compiler
  stays deterministic given seed + Spec
- Hermetic tests with pinned seeds; goldens pin seed where needed
- BACKLOG `#17e` → building

## Non-goals

- Per-place bias (Dover vs Cotentin)
- ME Dynamic / cyclone weather (`atmosphere_type=1`)
- Mid-flight cloud/rain/wind changes (`#17c` fog only later)
- Re-weather CLI/agent overwrite of existing `.miz` (`#17d` follow-on)
- Live METAR / online weather

## Capabilities

### New Capabilities

- `weather-invent`: invent-time weather snapshot resolution (gallery family,
  season/time priors, jitter, seed persistence)

### Modified Capabilities

- `mission-spec`: optional `weather_opts` with `seed`
- `miz-compiler`: apply resolved snapshot (4-layer wind where set; clamp base)
- `mission-validation`: accept `weather_opts`; seed rules
- `reference-registry`: pattern → allowed gallery family ids for priors
- `golden-fixtures` / weather SoT: pin seeds where emit must stay stable

## Impact

- `models.py`, `weather_presets.yaml` / registry, new invent module, compiler
  `_apply_weather`, examples/tests, catalog descriptions unchanged for pattern
  ids (class stays the same)
- Acceptance: compile two Specs same pattern different seeds → ME weather differs
  within class; same seed → identical; open `.miz` in ME

## Goal / Why (apply)

**Goal:** Always-on seeded Channel weather variation within pattern class.
**Why:** Realism without Dynamic cyclones; foundation for `#17d` re-weather.
