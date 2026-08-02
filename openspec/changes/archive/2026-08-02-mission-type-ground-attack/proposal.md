## Why

Intercept and CAP cover air-to-air Channel sorties, but the Spec still cannot express a
ground-attack: place ground targets, select a Spitfire bomb loadout, and compile a flyable
strike. Without this M4 slice, payload families stay `future` and the agent cannot plan
Channel CAS / bomb runs.

## What Changes

- Extend Mission Spec with `mission_type: ground_attack`, a typed strike block (airfield-
  relative target area, optional `practice` for allied bombing-practice targets), **enemy-
  only** combat `targets` (or same-coalition when practice), a named player payload preset,
  and a minimal `attack_ground` objective; keep `triggers` empty.
- Grow Channel registry: verified Spitfire bomb CLSID presets in `payloads.yaml` (including
  Channel-crossing presets with the 45 gal slipper tank), WWII enemy land units, and
  Channel ship/boat ids for over-water strikes.
- Compiler: cold Spitfire with registry loadout, GroundAttack tasking + ingress to the
  strike point, place enemy land **or** ship target groups (domain from registry); allow
  drop-tank jettison; free_flight / intercept / CAP unchanged. Land targets on enemy-held
  territory for the mission date; mid-Channel uses ships/boats only.
- Validation, planning-options/catalog (`ground_attack` + payload families supported),
  golden + example Spec; in-game accept the ground-attack `.miz`.
- Agent allow-list / schema tool / voice brief notes learn `ground_attack`.

## Non-goals

- Escort packages, briefing → `.miz` `l10n`, win/lose triggers / Lua (M6).
- Multi-theatre; Typhoon / non-Spitfire strikers; inventing CLSIDs or ground unit ids.
- Agent-invented WGS84 coords; new weather presets; full ME static scenery.
- Re-enabling PyDCS install payload directory scanning (apply known CLSIDs only).
- Named airfield/runway attack (`BombingRunway`) (deferred).
- Friendly or same-coalition strike targets (always rejected).
- Scripted / waypoint-triggered fuel-tank jettison (player jettisons in cockpit; AI
  auto-jettison-empty MAY be set; do not invent custom jettison Lua).

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / registry / options)*

### Modified Capabilities

- `mission-spec`: `ground_attack` type; strike block; enemy-only targets; payload; objective.
- `miz-compiler`: Compile ground-attack Spec (loadout + GroundAttack + enemy ground units).
- `mission-validation`: Validate strike/targets/payload; reject friendly/same-side targets.
- `golden-fixtures`: Ground-attack structural golden beside free-flight / intercept / CAP.
- `mission-options`: `ground_attack` supported; promote payload families from `future`.
- `reference-registry`: Payload presets + land units + ships as Channel SoT.
- `nl-agent` / `squadron-voice` / `agent-tools` (light): allow/list/schema/brief for GA.

## Impact

- `models.py`, registry YAML + API, `validation.py`, `pydcs_compiler.py`, planning_options,
  catalog sync, agent schema/voice, examples, goldens, docs/BACKLOG.
- Acceptance: open compiled ground-attack `.miz` in DCS ME / Instant Action (Channel +
  Spitfire + bombs + ground targets).
