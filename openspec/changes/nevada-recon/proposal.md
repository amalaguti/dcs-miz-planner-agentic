## Why

Nevada invent can fly five of six mission types, but recon still refuse-closes
every turn. Recon AOI is already airfield-relative. The Creech inland station
(303° / 85 km) is packaged as `creech_range_strike` — the analogue of Channel
recon 125° / 76 km, Caucasus recon 43° / 110 km, and Syria recon 121° / 200 km.
Do not copy french-coast geometry or CAP 350/40 onto a desert land observe.

## What Changes

- Ship `examples/nellis_creech_recon.yaml` (Nellis, Su-25T USA blue, observe
  Ural-375 trucks country Russia red at 303° / 85 km / 2000 m, radius_m 3000,
  mark true, weapons hold, no payload).
- Allow invent/chat **recon** on Nevada (all six types).
- Schema `theatre=Nevada` + `recon` loads the new example with dedicated notes
  (no french_coast / Manston 125/76 concatenation). Stub LLM stays Manston.
- Extend `creech_range_strike` `mission_types` with `recon`. Extend
  `nellis_home` with `recon`. Family stays `channel_place`. Do not add recon
  to `nellis_north_range_cap`.

## Non-goals

- Domain rewrite, intercept_spawn, path clamp, extra unit YAML, QAG scrape,
  `theatre_place` rename, dual-offer retag, Falklands combat.
- Changing Channel/Caucasus/Syria recon goldens or Nevada CAP 350/40.
- Adding recon to `nellis_north_range_cap`.
- ME Instant Action as a merge gate (human do-soon after merge).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `nl-agent`: Nevada invent includes recon (all six types).
- `agent-tools`: schema Nevada+recon example.
- `mission-options`: Creech inland place also cues recon.
- `mission-validation`: well-formed Nevada recon validates.
- `miz-compiler`: Nevada recon compiles; Channel recon goldens unchanged.

## Impact

Invent allow-table / schema / prompts, place mission_types, new example + tests.
Compiler already places recon via airfield-relative geometry. Domain already
classifies 303/85 land. Acceptance: ruff + pytest + compile the new example.
ME Instant Action is do-soon after merge.
