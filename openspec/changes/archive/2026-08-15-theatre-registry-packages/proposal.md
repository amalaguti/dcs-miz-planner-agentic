## Why

Normandy smoke is stuffed into a single `data/channel/` package with Channel
airfields. Airdrome ids are per-theatre, but lookup is a flat name map, so
Channel `Manston=5` could be applied on Normandy. Full-catalog maps need
per-theatre packages and a walker loader before any new bind.

## What Changes

- Split packaged YAML into `data/era/wwii/`, `data/shared/`, and
  `data/theatres/<SpecId>/` (`TheChannel`, `Normandy`). Delete `data/channel/`.
- Registry loader walks packages and merges era + shared + theatre tables.
- **BREAKING (API callers):** airfield lookup is theatre-scoped. Validate and
  compile MUST pass `spec.theatre`. Unscoped unique-name lookup remains for
  tests. Keep `ChannelRegistry` / `get_channel_registry()`.
- Re-home existing verified ids only. Keep the whole weather-presets file in
  `shared/` so Normandy smoke still resolves `sunny_clear`.
- Channel goldens and Needs Oar Point smoke stay green.

## Non-goals

- Slice 0b: invent prompts, country YAML, domain clamp, intercept spawn, path
  clamp, strike-unit theatre tags, reweather/METAR.
- New airfields, places, units, theatres, or Stage C combat.
- Bind `MarianaIslandsWWII` / `Kola` / `Iraq`.
- Moving PyDCS binds into YAML (`theatre_terrain.py` stays).
- Mass-rename of `ChannelRegistry`.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reference-registry`: SoT is packaged packages (era + shared + per-theatre),
  not a single `data/channel/` tree. Airfield lookup is theatre-scoped.
  Manston / Spitfire / Normandy / NeedsOarPoint scenarios remain.
- `mission-validation`: reject an airfield that is not in the Spec theatre
  (e.g. `Manston` with `theatre: Normandy`).
- `miz-compiler`: resolve player `airdromeId` from the Spec theatre’s airfield
  map, not a flat Channel+Normandy dict.

## Impact

`registry.py`, `validation.py`, `compiler/pydcs_compiler.py`, `reference.py`,
`target_motion.py`, `weather_gallery.py`; packaged YAML under `data/`; registry
and Normandy tests; README / ARCHITECTURE / lessons / `dcs-dev-channel-ids`.
Hatch already ships the whole `data/` tree. Acceptance: hermetic pytest +
compile Manston and Needs Oar Point examples. ME Instant Action on both maps
is do-soon after merge, not a merge blocker.
