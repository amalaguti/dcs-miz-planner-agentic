## Why

Caucasus can invent five of six mission types, but recon still refuse-closes every turn. Recon AOI is airfield-relative (same compiler path as Channel). The Colchis land station inland of Kutaisi (43° / 110 km) is already packaged as `kutaisi_inland_strike` — the analogue of Channel recon 125° / 76 km inland of Dunkirk and Normandy recon 180° / 133 km inland of Maupertus. Do not copy french-coast geometry or CAP 270/40 (sea) onto a land observe.

## What Changes

- Ship `examples/batumi_kutaisi_recon.yaml` (Batumi, Su-25T, observe Ural-375 trucks at 43° / 110 km / 2000 m, weapons hold).
- Allow invent/chat **recon** on Caucasus (all six types).
- Schema `theatre=Caucasus` + `recon` loads the new example with dedicated notes (no french_coast / Manston 125/76 concatenation).
- Extend `kutaisi_inland_strike` `mission_types` with `recon`. Extend `batumi_home` with `recon`. Family stays `channel_place`. Do not add recon to `batumi_black_sea_cap` (sea).

## Non-goals

- Path clamp on Caucasus, harbour/sea recon, extra unit YAML, QAG scrape, `theatre_place` rename, Syria/Nevada/Falklands combat.
- Changing Channel recon goldens (Manston 125/76) or Normandy recon 180/133.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Caucasus invent includes recon (all six types).
- `agent-tools`: schema Caucasus+recon example.
- `mission-options`: Kutaisi inland place also cues recon.
- `mission-validation`: well-formed Caucasus recon validates.
- `miz-compiler`: Caucasus recon compiles; Channel recon goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests. Compiler already places recon via airfield-relative geometry. Acceptance: ruff + pytest + compile the new example. ME Instant Action is do-soon after merge.
