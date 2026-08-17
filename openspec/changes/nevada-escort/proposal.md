## Why

Nevada invent can CAP and intercept on desert north-range (350° / 40 km from
Nellis), but escort still fail-closes every turn. Package destination is already
airfield-relative. That station is the land-transit analogue of Channel escort
120° / 55 km — do not copy Manston, Incirlik 180/40, Batumi 270/40, or
Cherbourg 180/63 onto Nevada.

## What Changes

- Ship `examples/nellis_north_range_escort.yaml` (Nellis, USA Su-25T escorting
  2× Su-25T to 350° / 40 km / 4000 m, light Russia Su-25T bounce). Explicit
  `package[].country: USA` and `enemies[].country: Russia`.
- Allow invent/chat **escort** on Nevada. GA and recon still refuse every turn.
- Schema `theatre=Nevada` + `escort` loads the new example with dedicated notes
  (no Manston 120/55 concatenation).
- Extend `nellis_north_range_cap` `mission_types` to include `escort` (same
  350/40 land station). Extend `nellis_home` with `escort`. Family stays
  `channel_place`.

## Non-goals

- Domain classifier, GA/recon, extra unit YAML, QAG scrape, `theatre_place`
  rename, Falklands combat.
- Changing Channel escort goldens (Manston 120/55) or intercept_spawn literals.
- Compiler escort rewrite (already airfield-relative).
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Nevada invent includes escort; GA/recon still refuse.
- `agent-tools`: schema Nevada+escort example.
- `mission-options`: north-range place also cues escort.
- `mission-validation`: well-formed Nevada escort validates; GA invent still
  rejected.
- `miz-compiler`: Nevada escort compiles; Channel escort goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler escort path is already theatre-agnostic. Channel escort goldens stay
bit-identical. Acceptance: ruff + pytest + compile the new example. ME Instant
Action is do-soon after merge.
