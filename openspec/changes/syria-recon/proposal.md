## Why

Syria invent can fly five of six mission types, but recon still refuse-closes
every turn. Recon AOI is already airfield-relative. The Aleppo inland station
(121° / 200 km) is packaged as `aleppo_inland_strike` — the analogue of Channel
recon 125° / 76 km and Caucasus recon 43° / 110 km. Do not copy french-coast
geometry or CAP 180/40 (sea) onto a land observe.

## What Changes

- Ship `examples/incirlik_aleppo_recon.yaml` (Incirlik, Su-25T, observe
  Ural-375 trucks at 121° / 200 km / 2000 m, weapons hold).
- Allow invent/chat **recon** on Syria (all six types).
- Schema `theatre=Syria` + `recon` loads the new example with dedicated notes
  (no french_coast / Manston 125/76 concatenation).
- Extend `aleppo_inland_strike` `mission_types` with `recon`. Extend
  `incirlik_home` with `recon`. Family stays `channel_place`. Do not add recon
  to `incirlik_iskenderun_cap` (sea).

## Non-goals

- Domain rewrite, intercept_spawn, path clamp, extra unit YAML, QAG scrape,
  `theatre_place` rename, Nevada/Falklands combat.
- Changing Channel recon goldens (Manston 125/76) or Caucasus recon 43/110.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Syria invent includes recon (all six types).
- `agent-tools`: schema Syria+recon example.
- `mission-options`: Aleppo inland place also cues recon.
- `mission-validation`: well-formed Syria recon validates.
- `miz-compiler`: Syria recon compiles; Channel recon goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler already places recon via airfield-relative geometry. Acceptance: ruff +
pytest + compile the new example. ME Instant Action is do-soon after merge.
