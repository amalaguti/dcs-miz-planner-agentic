## Why

Falklands invent can CAP and intercept on the South Atlantic corridor (150° /
40 km from Mount Pleasant), but escort still fail-closes every turn. Package
destination is already airfield-relative. That station is the sea analogue of
Channel escort 120° / 55 km — do not copy Manston, Nellis 350/40, Incirlik
180/40, Batumi 270/40, or Cherbourg 180/63 onto Falklands.

## What Changes

- Ship `examples/mount_pleasant_south_atlantic_escort.yaml` (MountPleasant, UK
  Su-25T escorting 2× Su-25T to 150° / 40 km / 4000 m, light Argentina Su-25T
  bounce). Explicit `package[].country: UK` and `enemies[].country: Argentina`.
- Allow invent/chat **escort** on Falklands. GA and recon still refuse every turn.
- Schema `theatre=Falklands` + `escort` loads the new example with dedicated
  notes (no Manston 120/55 concatenation).
- Extend `mount_pleasant_south_atlantic_cap` `mission_types` to include
  `escort` (same 150/40 sea station). Extend `mount_pleasant_home` with
  `escort`. Family stays `channel_place`.

## Non-goals

- Domain classifier, GA/recon, extra unit YAML, Chile, Port Stanley as home,
  `theatre_place` rename.
- Changing Channel escort goldens (Manston 120/55) or intercept_spawn literals.
- Compiler escort rewrite (already airfield-relative).
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Falklands invent includes escort; GA/recon still refuse.
- `agent-tools`: schema Falklands+escort example.
- `mission-options`: South Atlantic place also cues escort.
- `mission-validation`: well-formed Falklands escort validates; GA invent still
  rejected.
- `miz-compiler`: Falklands escort compiles; Channel escort goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler escort path is already theatre-agnostic. Channel escort goldens stay
bit-identical.
