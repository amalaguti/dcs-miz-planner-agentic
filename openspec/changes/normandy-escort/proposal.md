## Why

Normandy can invent CAP, ground_attack, and intercept, but escort still refuse-closes every turn. Package destination is already airfield-relative (compiler uses the player airport). The Cherbourg corridor (180° / 63 km from Needs Oar Point) is the sea-transit analogue of Channel escort 120° / 55 km — do not copy Manston bearings onto Normandy.

## What Changes

- Ship `examples/needs_oar_point_escort.yaml` (NeedsOarPoint, Spitfire escorting 2× MosquitoFBMkVI to 180° / 63 km / 4000 m, light Bf-109 bounce).
- Allow invent/chat **escort** on Normandy. Recon still refuses every turn.
- Schema `theatre=Normandy` + `escort` loads the new example with dedicated notes (no Manston 120/55 concatenation).
- Extend `cherbourg_channel_cap` `mission_types` with `escort` (same 180/63 sea station). Family stays `channel_place`.

## Non-goals

- Recon, path clamp, harbour/sea GA, extra unit YAML, QAG scrape, `theatre_place` rename, Caucasus/Syria/Nevada/Falklands combat.
- Changing Channel escort goldens (Manston 120/55).
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Normandy invent includes escort; recon still refuses.
- `agent-tools`: schema Normandy+escort example.
- `mission-options`: Cherbourg place also cues escort.
- `mission-validation`: well-formed Normandy escort validates.
- `miz-compiler`: Normandy escort compiles; Channel escort goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests. Compiler already places escort via airfield-relative `point_from_heading`. Acceptance: ruff + pytest + compile the new example. ME Instant Action is do-soon after merge.
