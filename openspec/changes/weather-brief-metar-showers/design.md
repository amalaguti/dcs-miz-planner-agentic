## Context

`#17a` / `#17e` ship named Channel weather recipes with invent snapshots
(`WeatherSnapshot`) and prose registry descriptions in briefs. Upstream
dcs-real-weather maps METAR coverage → gallery presets and can *generate* a
METAR from applied weather (`DecodePreset` + `GenerateMETAR`). We prefer recipes
over live METAR (BACKLOG `#17a`/`#17e`); R10 notes in gitignored
`research/weather.md` now hold their `CloudPresets` / `DecodePreset` tables for
audit. Gap: no light-rain / showers Spec pattern (`RainyPreset4`–`6` /
`NEWRAINPRESET4`), and briefs never emit a METAR-looking line from the snapshot.

## Goals / Non-Goals

**Goals:**

- Deterministic synthetic METAR string from `WeatherSnapshot` + Spec date/time
  (offline), injected into commander brief and thus compile `l10n` briefing.
- New Spec pattern `showers_scattered` (light rain / Channel showery day) with
  gallery family covering rainy light presets; invent stays within family.
- Keep weather SoT parity green across enum / YAML / planning_options / compiler.

**Non-Goals:**

- Live meteo APIs; dcs-real-weather binary; dust/TS precip beyond gallery.
- Spec field for arbitrary ICAO (fixed synthetic station for Channel briefs).
- Changing fog_dynamics, re-weather UX, or invent seed semantics.

## Decisions

1. **Pattern id `showers_scattered`** — pilot-facing “showery / light rain under
   broken–scattered”; family
   `[RainyPreset4, NEWRAINPRESET4, RainyPreset5, RainyPreset6]` (upstream
   SCT+RA / BKN+RA / light OVC+RA). Default recipe center: `RainyPreset4`.
   Keep `rain_overcast` on `RainyPreset1`–`3` only (no silent merge).
   - Alternative: split SCT vs BKN light-rain patterns — deferred (one pattern
     + invent family is enough for Channel feel).

2. **METAR builder module** (e.g. `weather_metar.py`) — pure function
   `format_synthetic_metar(snap, spec, *, icao="EGMH") -> str` using packaged
   decode table (YAML or const mirrored from R10 research). Wind kt from
   ground layer; vis SM from snapshot visibility; temp/dewpoint (dewpoint
   heuristic from temp + fog/vis); QNH mmHg → inHg Axxxx; cloud groups from
   decode + first-layer base from `clouds_base_m`. Append `NOSIG` + optional
   `RMK SIM` (or similar) so pilots know it is not a live observation.
   - Alternative: LLM-authored METAR — rejected (non-hermetic, invents ids).

3. **Brief injection** — `build_commander_brief` / meteo helper appends one
   METAR line under Situation (or a short “Met” line after weather prose). Same
   string flows to `mission-briefing` via existing brief split. No Spec field
   change for METAR content.
   - Alternative: only Description, not CLI brief — rejected (voice + compile
     must stay shared).

4. **Decode table packaging** — ship a small Channel data file (or section of
   `weather_presets.yaml`) mapping gallery id → cloud layer codes/bases for
   METAR; unknown gallery / legacy density → `CLR` or density-derived single
   group. Research copy in `research/weather.md` remains gitignored audit SoT.
   - Alternative: hardcode only rainy presets — rejected (METAR useful for all
     gallery patterns).

5. **ICAO** — fixed `EGMH` (Manston) for Channel synthetic line unless a later
   change maps airfield→ICAO from registry. Do not invent unverified ICAOs per
   spawn.

6. **Tests** — unit tests for METAR determinism (pinned seed); SoT parity picks
   up new enum; optional example Spec `showers_scattered`; ME smoke acceptance
   as for other weather patterns.

## Risks / Trade-offs

- [Risk] Synthetic METAR misread as live → Mitigation: `RMK SIM` (or voice prose
  “synthetic metar”) + docs/BACKLOG note no live METAR
- [Risk] `NEWRAINPRESET4` id missing on older PyDCS → Mitigation: validate via
  `CloudPreset.by_name` in tests; fall back family without it if absent
- [Risk] Dewpoint heuristic wrong → Mitigation: document as approximate; clamp
  dew ≤ temp; prefer fog/vis cues
- [Risk] Brief length / golden drift → Mitigation: contract asserts substring
  `EGMH` / `NOSIG`; refresh goldens only when intentional

## Migration Plan

- Existing Specs unchanged; new pattern opt-in via `weather: showers_scattered`.
- METAR appears on all briefs once implemented (additive text).
- Rollback: remove pattern id + METAR call; restore prior brief wording.

## Open Questions

- None blocking; airfield→ICAO mapping deferred.
