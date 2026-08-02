## Why

Intercept, CAP, and ground-attack cover scramble, patrol, and strike, but the Spec still
cannot express a Channel **escort**: protect a friendly package along a route with optional
enemy bounce. Without this last M4 type, the agent cannot plan classic Spitfire escort
sorties, and M5 briefing work stays blocked on unfinished mission types.

## What Changes

- Extend Mission Spec with `mission_type: escort`, a nested `escort` block (airfield-relative
  package destination / altitude + engagement ROE), a required non-empty **friendly**
  `package` list (same coalition as the player), optional opposing `enemies`, and a minimal
  `escort_package` objective; keep `triggers` empty; no ground `targets` / `strike` /
  player payload for escort v1.
- Compiler: cold Spitfire with Escort task + `EscortTaskAction` linked to the package group;
  place the package AI flight on a Channel route to the Spec destination; optional bandits
  near the route; free_flight / intercept / CAP / ground_attack unchanged.
- Validation, planning-options/catalog (`escort` supported), golden + example Spec; in-game
  accept the escort `.miz`.
- Agent allow-list / schema tool / voice brief notes learn `escort`.
- Registry: add at least one verified package aircraft beyond fighters if the example needs
  it (exact PyDCS id only); radio defaults as for other aircraft.

## Non-goals

- Briefing → `.miz` `l10n` (`briefing-generation` / M5); win/lose triggers / Lua (M6).
- Multi-theatre; player wingmen as separate controllable flights; formation editor UI.
- Agent-invented WGS84 coords or aircraft ids; new weather presets.
- Escorting ground columns / ships (air package only in v1).
- Package bomb loadouts / strike target placement on the escort Spec (package flies a route;
  strike detail stays ground_attack).
- Re-enabling PyDCS install payload directory scanning.

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / options / agent surfaces)*

### Modified Capabilities

- `mission-spec`: `escort` type; escort block; friendly package; optional enemies; objective.
- `miz-compiler`: Compile escort Spec (package route + Escort task + optional bounce).
- `mission-validation`: Validate escort/package/enemies coalition and registry aircraft.
- `golden-fixtures`: Escort structural golden beside existing mission types.
- `mission-options`: `mission_type: escort` supported.
- `reference-registry`: Package aircraft ids / radios as needed for the example.
- `nl-agent` / `squadron-voice` / `agent-tools` (light): allow/list/schema/brief for escort.

## Impact

- `models.py`, registry YAML (if new package aircraft), `validation.py`,
  `compiler/pydcs_compiler.py`, planning_options, catalog sync, agent schema/voice,
  examples, goldens, docs/BACKLOG.
- Acceptance: open compiled escort `.miz` in DCS ME / Instant Action (Channel + Spitfire +
  friendly package + optional bandits).
