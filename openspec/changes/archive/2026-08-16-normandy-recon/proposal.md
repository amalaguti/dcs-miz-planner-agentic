## Why

Normandy can invent five of six mission types, but recon still refuse-closes every turn. Recon AOI is airfield-relative (same compiler path as Channel). The Cotentin land station inland of Maupertus (180° / 133 km) is already packaged as `maupertus_inland_strike` — the analogue of Channel recon 125° / 76 km inland of Dunkirk. Do not copy french-coast geometry or CAP 180/63 (sea) onto a land observe.

## What Changes

- Ship `examples/needs_oar_point_recon.yaml` (NeedsOarPoint, Spitfire, observe Blitz trucks at 180° / 133 km / 2000 m, weapons hold).
- Allow invent/chat **recon** on Normandy (all six types).
- Schema `theatre=Normandy` + `recon` loads the new example with dedicated notes (no french_coast / Manston 125/76 concatenation).
- Extend `maupertus_inland_strike` `mission_types` with `recon`. Family stays `channel_place`.

## Non-goals

- Path clamp on Normandy, harbour/sea recon, extra unit YAML, QAG scrape, `theatre_place` rename, Caucasus/Syria/Nevada/Falklands combat.
- Changing Channel recon goldens (Manston 125/76).
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Normandy invent includes recon (all six types).
- `agent-tools`: schema Normandy+recon example.
- `mission-options`: Maupertus inland place also cues recon.
- `mission-validation`: well-formed Normandy recon validates.
- `miz-compiler`: Normandy recon compiles; Channel recon goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests. Compiler already places recon via airfield-relative geometry. Acceptance: ruff + pytest + compile the new example. ME Instant Action is do-soon after merge.
