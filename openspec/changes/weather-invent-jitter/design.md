## Context

`#17a` shipped named Channel patterns with fixed YAML recipes (gallery id +
numerics for expanded ids; density path for the trio). Compiler
`_apply_weather` applies recipes deterministically. Explore (2026-08-06)
locked always-on invent variation, hybrid gallery+nudge, no place bias,
`weather` + `weather_opts.seed` with auto-write. Climatology notes live in
gitignored `research/weather.md` (Channel seasonal signatures only).

## Goals / Non-Goals

**Goals:**

- Resolve a concrete weather snapshot from pattern + date + start_time + seed
- Within-family gallery preference + soft numeric nudge + jitter
- Persist seed on Spec YAML when compile/invent has a writable Spec path
- Keep pattern class stable (rain stays rain family)
- Shared snapshot type usable later by `#17d` re-weather

**Non-Goals:**

- Place bias; ME Dynamic; mid-flight weather; `#17d` CLI/agent in this change

## Decisions

1. **Module `weather_invent.py`** — pure function
   `resolve_weather_snapshot(spec, seed) -> WeatherSnapshot` (gallery id or
   legacy density fields + numerics including up to four wind layers). Compiler
   applies snapshot only (no RNG in compiler).
   - Alternative: jitter inside `_apply_weather` — rejected (harder to test /
     reuse for `#17d`).

2. **`weather_opts: { seed?: int }`** — optional nested model; keep top-level
   `weather: WeatherPreset` enum (non-breaking).
   - Alternative: nested `weather: { preset, seed }` — deferred (breaking).

3. **Auto-write seed** — when seed omitted and invent/compile writes Spec
   sidecar (or invent step before compile), draw seed and persist. Hermetic
   tests and goldens **must** set explicit seeds.
   - If reproducibility feels wrong → re-weather with new seed (`#17d`).

4. **Hybrid priors** — each pattern maps to an allowed gallery family list in
   YAML/registry. Season (from `date.month`) + coarse time-of-day (from
   `start_time`) weight the pick; then nudge temp/wind/fog/base/QNH/turb within
   bands; clamp base to `CloudPreset` min/max. Legacy trio: no gallery swap;
   numeric nudge only (or light density jitter within safe bounds).
   - Cross-family swaps only via changing Spec `weather`.

5. **Wind layers** — snapshot may set ground + aloft (PyDCS wind_at_ground /
   2000 / 8000 as available); invent fills from recipe ground + seasonal shear
   heuristics when aloft omitted.

6. **Randomize axis** — `randomize` weather axis still picks pattern id; invent
   jitter remains separate (always on at compile with seed).

## Risks / Trade-offs

- [Risk] Goldens drift if seed omitted → Mitigation: pin `weather_opts.seed` on
  examples used in goldens; refresh only if intentional
- [Risk] Gallery family lists drift from PyDCS → Mitigation: validate ids via
  `CloudPreset.by_name` in tests
- [Risk] Over-strong season weights make July rain feel wrong → Mitigation:
  keep within-family only; mild weights; tune from ME smoke
- [Risk] Auto-write needs Spec path → Mitigation: if compile from in-memory
  Spec only, seed in returned/written YAML when path known; document

## Migration Plan

- Existing Specs without `weather_opts` keep loading; first compile with invent
  assigns seed when writing YAML
- Rollback: feature-flag or skip invent and apply recipe centers only

## Open Questions

- None blocking; place bias explicitly out; `#17d` consumes snapshot later
