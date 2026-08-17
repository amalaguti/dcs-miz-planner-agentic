## Why

Syria invent can CAP and intercept on the Gulf of Iskenderun (180° / 40 km
south of Incirlik), but escort still fail-closes every turn. Package destination
is already airfield-relative. The Iskenderun station is the sea-transit analogue
of Channel escort 120° / 55 km — do not copy Manston, Cherbourg 180/63, or
Batumi 270/40 onto Syria.

## What Changes

- Ship `examples/incirlik_iskenderun_escort.yaml` (Incirlik, Turkey Su-25T
  escorting 2× Su-25T to 180° / 40 km / 4000 m, light Syria Su-25T bounce).
  Explicit `package[].country: Turkey` and `enemies[].country: Syria`.
- Allow invent/chat **escort** on Syria. GA and recon still refuse every turn.
- Schema `theatre=Syria` + `escort` loads the new example with dedicated notes
  (no Manston 120/55 concatenation).
- Extend `incirlik_iskenderun_cap` `mission_types` to include `escort` (same
  180/40 sea station). Extend `incirlik_home` with `escort`. Family stays
  `channel_place`.

## Non-goals

- Domain classifier, GA/recon, extra unit YAML, QAG scrape, `theatre_place`
  rename, Nevada/Falklands combat.
- Changing Channel escort goldens (Manston 120/55) or intercept_spawn literals.
- Compiler escort rewrite (already airfield-relative).
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Syria invent includes escort; GA/recon still refuse.
- `agent-tools`: schema Syria+escort example.
- `mission-options`: Iskenderun place also cues escort.
- `mission-validation`: well-formed Syria escort validates; GA invent still
  rejected.
- `miz-compiler`: Syria escort compiles; Channel escort goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler escort path is already theatre-agnostic. Channel escort goldens stay
bit-identical. Acceptance: ruff + pytest + compile the new example. ME Instant
Action is do-soon after merge.
