## Why

Caucasus Stage B curated eight airfields and Mozdok smoke, but invent is still
free_flight only. CAP is already airfield-relative and compiles without a domain
classifier or intercept spawn. Stage C adds Batumi place recipes and CAP invent
so the NL agent can plan a Black Sea CAP from Batumi.

## What Changes

- Add `channel_place` rows `batumi_home` and `batumi_black_sea_cap`
  (`meta.theatre: Caucasus`; CAP station 270° / 40 km / 4000 m west of Batumi).
  Family name stays `channel_place` (no `theatre_place` rename).
- Ship `examples/batumi_black_sea_cap.yaml` (Batumi, Georgia, Su-25T, 2024-06-06
  `sunny_clear`, Russia Su-25T red opposition). Explicit `enemies[].country:
  Russia` (model default is `ThirdReich`).
- Lift invent/chat refuse for **CAP only**. Intercept / ground_attack / escort /
  recon stay every-turn refuse. Schema `theatre=Caucasus` + `cap` uses the new
  example (no Manston / NeedsOarPoint skeleton).
- `list_mission_options(theatre=Caucasus)` already filters `channel_place` by
  `meta.theatre`; new rows must not leak into Channel/Normandy filters.

## Non-goals

- Domain classifier, intercept spawn, path clamp, GA/recon examples, extra
  airfields, extra unit YAML, paid FC3 jets, Spitfire as the CAP smoke aircraft,
  `theatre_place` rename, Syria/Nevada/Falklands combat.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Caucasus invent is free_flight **or CAP**; other combat types
  still refuse; do not copy Channel/Normandy geometry onto Caucasus.
- `agent-tools`: schema Caucasus+CAP example.
- `mission-options`: two Caucasus `channel_place` rows.
- `agent-catalog`: catalog lists the new places after sync.
- `miz-compiler`: Batumi CAP compiles (N1-style contracts).
- `mission-validation`: Batumi CAP validates; intercept/domain still fail-closed.

## Impact

`planning_options.yaml`, invent nudge/schema/prompts, new CAP example + tests.
Domain, intercept spawn, and path clamp stay as today. Channel goldens stay
green. Acceptance: hermetic pytest + compile the new CAP example. ME Instant
Action on Batumi CAP is do-soon after merge.
