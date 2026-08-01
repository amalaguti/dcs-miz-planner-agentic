## Why

Intercept proved combat Spec + compile, but the next M4 story is a Channel CAP: patrol a
station with clear engagement rules. Without this slice, the agent and Spec stay limited to
scramble-or-free-flight, and `roe_seed` planning options remain forever-`future`.

## What Changes

- Extend Mission Spec with `mission_type: cap`, a typed CAP block (patrol station, altitude,
  pattern, optional duration), and engagement/ROE as a real Spec field (promote from
  planning-option `future`).
- Add a minimal CAP objective type (e.g. `patrol`); keep `triggers` empty.
- CAP MAY include optional `enemies` (empty = pure patrol; non-empty = hostiles near station).
  Free flight and intercept rules unchanged.
- Compiler: player cold start + nav/CAP waypoints (Orbit) at a documented Channel station;
  apply group ROE; place optional enemies with existing inflight helpers.
- Validation, planning-options/catalog (`cap` supported; ROE supported for CAP), golden +
  example Spec; in-game accept the CAP `.miz`.
- Agent allow-list / voice brief notes learn `cap` (no NL redesign).

## Non-goals

- Ground-attack, escort, briefing → `.miz` `l10n` (`briefing-generation` waits until M4 types
  finish).
- Full trigger / win-lose graph (M6); Mist/MOOSE; multi-theatre; wingman AI packages.
- Arbitrary WGS84 lat/lon from the agent; inventing DCS ids.
- New weather presets; Normandy.

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / golden-fixtures / options)*

### Modified Capabilities

- `mission-spec`: `cap` mission type; CAP station/ROE fields; optional enemies; patrol objective.
- `miz-compiler`: Compile CAP Spec (waypoints/Orbit + ROE + optional enemies); other types unchanged.
- `mission-validation`: Validate CAP combinations via registry; refuse bad station/ROE/objective.
- `golden-fixtures`: CAP structural golden alongside free-flight and intercept.
- `mission-options`: `mission_type: cap` supported; `roe_seed` → supported Spec-backed ROE.
- `nl-agent` / `squadron-voice` (light): allow `cap` in planning rules / brief tactics when present.

## Impact

- `models.py`, `validation.py`, `compiler/pydcs_compiler.py`, `planning_options.yaml`, catalog
  sync, agent prompts/voice CAP tactics, examples, tests/fixtures, docs/BACKLOG.
- Acceptance: open compiled CAP `.miz` in DCS ME / Instant Action (Channel + Spitfire).
