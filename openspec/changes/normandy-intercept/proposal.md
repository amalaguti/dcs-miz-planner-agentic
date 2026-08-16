## Why

Normandy can invent CAP and ground_attack, but intercept still fail-closes on Hawkinge/Dover literals. The Cherbourg corridor (180° / 63 km from Needs Oar Point) is already a packaged sea place. This slice adds that recipe so WWII intercept colour works on Normandy without copying Channel spawn.

## What Changes

- Add a Normandy intercept spawn recipe: Needs Oar Point map position plus due-south 63 km offset (PyDCS `point_from_heading(180, 63000)`). Store literals; do not recompute Channel Hawkinge from `airport_list()`.
- Ship `examples/needs_oar_point_dawn_intercept.yaml` (NeedsOarPoint, Spitfire, Bf-109K-4, 06:00, `sunny_clear`, 1944-06-06).
- Allow invent/chat **intercept** on Normandy. Escort / recon still refuse every turn.
- Schema `theatre=Normandy` + `intercept` loads the new example with dedicated notes (no Hawkinge concatenation).
- Extend `cherbourg_channel_cap` `mission_types` to include `intercept` (same 180/63 sea station). Family stays `channel_place`.

## Non-goals

- Escort, recon, path clamp, harbour/sea GA, extra unit YAML, QAG scrape, `theatre_place` rename, Caucasus/Syria/Nevada/Falklands combat.
- Changing Channel Hawkinge/Dover goldens.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Normandy invent is free_flight, CAP, ground_attack, **or intercept**; escort/recon still refuse.
- `agent-tools`: schema Normandy+intercept example.
- `mission-options`: Cherbourg place also cues intercept.
- `mission-validation`: well-formed Normandy intercept validates.
- `miz-compiler`: Normandy intercept compiles; Channel Hawkinge recipe unchanged.

## Impact

`intercept_spawn.py`, invent allow-table / schema / prompts, validation hint, new example + tests. Channel intercept goldens stay bit-identical. Acceptance: ruff + pytest + compile the new example. ME Instant Action is do-soon after merge.
