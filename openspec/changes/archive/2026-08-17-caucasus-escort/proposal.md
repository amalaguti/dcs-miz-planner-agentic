## Why

Caucasus invent can intercept and bomb inland of Kutaisi, but escort still
refuse-closes every turn. Package destination is already airfield-relative
(compiler uses the player airport). The Black Sea CAP station (270° / 40 km
west of Batumi) is the sea-transit analogue of Channel escort 120° / 55 km —
do not copy Manston bearings onto Caucasus.

## What Changes

- Ship `examples/batumi_black_sea_escort.yaml` (Batumi, Georgia Su-25T escorting
  2× Su-25T to 270° / 40 km / 4000 m, light Russia Su-25T bounce). Explicit
  `package[].country: Georgia` and `enemies[].country: Russia`.
- Allow invent/chat **escort** on Caucasus. Recon still refuses every turn.
- Schema `theatre=Caucasus` + `escort` loads the new example with dedicated notes
  (no Manston 120/55 concatenation).
- Extend `batumi_black_sea_cap` `mission_types` to include `escort` (same 270/40
  sea station). Extend `batumi_home` with `escort`. Family stays `channel_place`.

## Non-goals

- Recon, path clamp, extra unit YAML, QAG scrape, `theatre_place` rename,
  Syria/Nevada/Falklands combat.
- Changing Channel escort goldens (Manston 120/55) or intercept_spawn literals.
- Compiler escort rewrite (already airfield-relative).
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Caucasus invent includes escort; recon still refuses.
- `agent-tools`: schema Caucasus+escort example.
- `mission-options`: Batumi Black Sea place also cues escort.
- `mission-validation`: well-formed Caucasus escort validates; recon invent still
  rejected.
- `miz-compiler`: Caucasus escort compiles; Channel escort goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler escort path is already theatre-agnostic. Channel escort goldens stay
bit-identical. Acceptance: ruff + pytest + compile the new example. ME Instant
Action is do-soon after merge.
