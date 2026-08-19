## Why

R3 was still research-only. Three colour cards already exist (Rhubarb, dawn recce,
Mustang). Channel campaigns and Spitfire IA on disk already fly Mosquito packages,
E-boat/cargo shipping, and a V-1 ski — invent cannot name Circus / Rodeo /
Channel Stop / Noball until those patterns are packaged as advisory inspiration.

## What Changes

- Gitignored research notes: web Fighter Command names **and** local campaign/IA
  `.miz` type scans (not Spec import).
- Four advisory `mission_inspiration` cards: `circus_escort`, `rodeo_sweep`,
  `channel_stop_shipping`, `noball_ski`. Spitfire UK default. Meta only cites
  existing Spec types, places, classes, unit ids.
- Prompt + eval catalog so vague “Circus” / “Noball” asks hit those cards.
- BACKLOG R3 `idea` → `done`.

## Non-goals

- New mission types, Lua, historical-validation engine, extra Mustang fly cards.
- Importing `.miz` as Spec. New weather YAML. Instant Action as merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `mission-options`: four historical inspiration cards.
- `nl-agent`: prompt maps Circus/Rodeo/Channel Stop/Noball to those cards.
- `golden-fixtures` / catalog tests: cards listable after sync.

## Impact

`planning_options.yaml`, agent prompt, eval catalog, tests, BACKLOG. Research
file stays gitignored.
