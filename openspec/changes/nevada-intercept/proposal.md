## Why

Nevada invent can fly CAP on desert north-range (350° / 40 km from Nellis), but
intercept still fail-closes. The packaged CAP station is already a land place.
This slice adds that spawn recipe so modern intercept colour works on Nevada
without copying Channel, Normandy, Caucasus, or Syria spawn.

## What Changes

- Add a Nevada intercept spawn recipe: Nellis map position plus heading 350° /
  40 km offset (PyDCS `point_from_heading(350, 40000)`). Store literals; do not
  recompute Channel Hawkinge from `airport_list()`.
- Ship `examples/nellis_dawn_intercept.yaml` (Nellis, USA, Su-25T, 06:00,
  `sunny_clear`, 2024-06-06). Explicit `enemies[].country: Russia`.
- Allow invent/chat **intercept** on Nevada. GA / escort / recon still refuse.
- Schema `theatre=Nevada` + `intercept` loads the new example with dedicated notes.
- Extend `nellis_north_range_cap` and `nellis_home` `mission_types` with
  `intercept`. Family stays `channel_place`.

## Non-goals

- Domain classifier, GA/escort/recon, extra unit YAML, extra countries,
  Falklands combat, Channel Hawkinge/Dover goldens.
- Copying Incirlik 180/40, Batumi 270/40, Cherbourg 180/63, or Hawkinge onto
  Nellis.
- ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Nevada invent is free_flight, CAP, **or intercept**.
- `agent-tools`: schema Nevada+intercept example.
- `mission-options`: north-range place also cues intercept.
- `mission-validation`: well-formed Nevada intercept validates; Falklands still fail-closed.
- `miz-compiler`: Nevada intercept compiles; Channel Hawkinge recipe unchanged.

## Impact

`intercept_spawn.py`, invent allow-table / schema / prompts, new example + tests.
Channel intercept goldens stay bit-identical.
