## Why

Falklands invent can fly CAP on the South Atlantic corridor (150° / 40 km from
Mount Pleasant), but intercept still fail-closes. The packaged CAP station is
already a sea place. This slice adds that spawn recipe so modern intercept
colour works on Falklands without copying Channel, Normandy, Caucasus, Syria,
or Nevada spawn.

## What Changes

- Add a Falklands intercept spawn recipe: Mount Pleasant map position plus
  heading 150° / 40 km offset (PyDCS `point_from_heading(150, 40000)`). Store
  literals; do not recompute Channel Hawkinge from `airport_list()`.
- Ship `examples/mount_pleasant_dawn_intercept.yaml` (MountPleasant, UK,
  Su-25T, 06:00, `sunny_clear`, 2024-06-06). Explicit
  `enemies[].country: Argentina`.
- Allow invent/chat **intercept** on Falklands. GA / escort / recon still refuse.
- Schema `theatre=Falklands` + `intercept` loads the new example with dedicated
  notes.
- Extend `mount_pleasant_south_atlantic_cap` and `mount_pleasant_home`
  `mission_types` with `intercept`. Family stays `channel_place`.
- Derive the `intercept_unsupported_theatre` hint from `INTERCEPT_SPAWN_RECIPES`
  keys (today it still lists only TheChannel, Normandy, or Caucasus).

## Non-goals

- Domain classifier, GA/escort/recon, extra unit YAML, extra countries, Chile,
  Port Stanley as home, Channel Hawkinge/Dover goldens.
- Copying Nellis 350/40, Incirlik 180/40, Batumi 270/40, Cherbourg 180/63, or
  Hawkinge onto Mount Pleasant. A new intercept heading.
- ME Instant Action as a merge gate.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Falklands invent is free_flight, CAP, **or intercept**.
- `agent-tools`: schema Falklands+intercept example.
- `mission-options`: South Atlantic place also cues intercept.
- `mission-validation`: well-formed Falklands intercept validates; hint lists
  recipe keys.
- `miz-compiler`: Falklands intercept compiles; Channel Hawkinge recipe
  unchanged.

## Impact

`intercept_spawn.py`, invent allow-table / schema / prompts, validation hint,
new example + tests. Channel intercept goldens stay bit-identical.
