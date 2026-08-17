## Why

Syria invent can fly CAP on the Gulf of Iskenderun (180° / 40 km south of
Incirlik), but intercept still fail-closes. The packaged CAP station is already
a sea place. This slice adds that spawn recipe so modern intercept colour works
on Syria without copying Channel, Normandy, or Caucasus spawn.

## What Changes

- Add a Syria intercept spawn recipe: Incirlik map position plus due-south 40 km
  offset (PyDCS `point_from_heading(180, 40000)`). Store literals; do not
  recompute Channel Hawkinge from `airport_list()`.
- Ship `examples/incirlik_dawn_intercept.yaml` (Incirlik, Turkey, Su-25T,
  06:00, `sunny_clear`, 2024-06-06). Explicit `enemies[].country: Syria`.
- Allow invent/chat **intercept** on Syria. GA / escort / recon still refuse.
- Schema `theatre=Syria` + `intercept` loads the new example with dedicated notes.
- Extend `incirlik_iskenderun_cap` and `incirlik_home` `mission_types` with
  `intercept`. Family stays `channel_place`.

## Non-goals

- Domain classifier, GA/escort/recon, extra unit YAML, extra countries,
  Nevada/Falklands combat, Channel Hawkinge/Dover goldens.
- Copying Batumi 270/40 or Cherbourg 180/63 onto Incirlik.
- ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Syria invent is free_flight, CAP, **or intercept**.
- `agent-tools`: schema Syria+intercept example.
- `mission-options`: Iskenderun place also cues intercept.
- `mission-validation`: well-formed Syria intercept validates; Nevada still fail-closed.
- `miz-compiler`: Syria intercept compiles; Channel Hawkinge recipe unchanged.

## Impact

`intercept_spawn.py`, invent allow-table / schema / prompts, new example + tests.
Channel intercept goldens stay bit-identical.
