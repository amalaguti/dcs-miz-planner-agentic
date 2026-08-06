## Why

After generating and loading a sortie, pilots often want different weather without
rebuilding groups/triggers. Today that requires hand-editing the Spec and
recompiling, or ME tweaks. A first-class re-weather path (CLI + agent) overwrites
the same `.miz` using `#17a`/`#17e` invent snapshots.

## What Changes

- Library + CLI `dcs-miz weather-set` (or equivalent): set weather pattern on an
  existing mission path; **overwrite** the `.miz`
- Prefer sibling Spec YAML (same stem) → update `weather` (+ new `weather_opts.seed`
  by default) → recompile over the `.miz`
- Fallback: PyDCS `Mission.load_file` → apply invent weather snapshot → `save`
- Agent tool wrapping the same API; discover sidecar or accept explicit paths
- Refresh briefing weather phrasing when Spec recompile path runs
- BACKLOG `#17d` → building

## Non-goals

- Mid-flight weather changes (`#17c`)
- ME Dynamic cyclones
- Round-tripping arbitrary ME-edited missions into a perfect Spec
- Sibling output files (overwrite decided)

## Capabilities

### New Capabilities

- `weather-reweather`: re-weather existing `.miz` / Spec sidecar (overwrite)

### Modified Capabilities

- `agent-tools`: tool to re-weather a mission path
- `miz-compiler` / `weather-invent`: shared snapshot apply on loaded Mission
  (if extract needed)

## Impact

- New module or functions under `weather_invent` / `tools` / `cli`
- PyDCS load/save path; invent seed behaviour from `#17e`
- Acceptance: change weather on a compiled example, overwrite, open in ME — weather
  differs, groups intact; reload ME if file was open

## Goal / Why (apply)

**Goal:** Overwrite an existing `.miz` with a new named weather pattern (invent jitter).
**Why:** Agent/pilot loop — same sortie, different Channel weather without rebuild.
