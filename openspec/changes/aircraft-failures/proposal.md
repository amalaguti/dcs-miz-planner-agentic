## Why

Training and “keep me honest” sorties need optional **aircraft failures** (engine,
controls, systems). Today the Spec cannot declare them; authors must hand-edit ME.
Channel Spitfire failure ids are known from stock `.miz` `failures` tables — curate
them; never free-form LLM strings. Stock missions arm the ME Failures panel table
(not trigger `a_set_failure`).

## What Changes

- Spec: optional top-level `failures` list (omit/empty = none). Each entry: curated
  `id`, `start_after_s`, optional `probability` (default 100) and `random_pause_s`
  (default 0) — maps to Failures panel After / Within (minutes) / probability.
- Registry/YAML catalog of allowed SpitfireLFMkIX failure ids (engine / controls /
  fuel / hydraulics subset first; full ME dump not required in v1).
- Validation: reject unknown ids / bad ranges; only when player aircraft has a catalog.
- Compiler: write `mission.failures` rows (`enable`/`hh`/`mm`/`mmint`/`prob`); no Lua;
  no `a_set_failure` triggers.
- Brief/voice honesty when failures are armed; example + structural tests; planning
  options / schema notes.
- Acceptance: ME Failures panel shows armed ids; Instant Action smoke (magneto drill).

## Non-goals

- Free-form failure strings; LLM-authored Lua; multipayer Client failures.
- Full Spitfire ME failure dump as Spec surface (curate; expand later).
- Flag-random “pick from pool” as a separate mode (use per-entry probability /
  Within first; `#22a` pool later if needed).
- Failures on AI wingmen / package (player aircraft only in v1).
- Relying on Options → Misc → Random System Failures for scripted cuts.

## Capabilities

### New Capabilities

- *(none — extend existing surfaces)*

### Modified Capabilities

- `mission-spec`: optional `failures` list.
- `miz-compiler`: emit Failures panel table rows.
- `mission-validation`: curated id + range checks.
- `reference-registry`: Spitfire failure id catalog (YAML + API).
- `golden-fixtures` / structural tests for Failures table emit.
- `mission-options` / `nl-agent` / `mission-briefing` / `squadron-voice` (light):
  failure knobs and brief honesty.

## Impact

- `models.py`, validation, compiler emit, Channel data YAML, examples, tests,
  BACKLOG `#22b`.
- Acceptance: open compiled `.miz` in ME; confirm Failures panel; fly optional smoke.
