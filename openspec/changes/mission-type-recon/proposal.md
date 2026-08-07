## Why

Channel Specs can fly free flight, intercept, CAP, ground attack, and escort, but cannot
express a locate/observe sortie: fly to an area or contact, report it, and RTB **without**
strike payload or destroy win conditions. Recon is the remaining M4 mission type that needs
distinct validate/compile rules from GA-with-empty-bombs.

## What Changes

- Add `mission_type: recon` with a nested `recon` block (airfield-relative AOI geometry +
  altitude + observe radius), objective `recon_area`, and optional enemy `targets` as
  **visual contacts only** (no attack tasking / no payload).
- Forbid `player.payload`, `strike`, `cap`, and `escort` on recon; keep air `enemies`
  empty in v1 (optional bounce deferred).
- Compiler: player cold Spitfire with PyDCS `Reconnaissance` tasking, ingress to AOI,
  Spec zone (+ optional F10 mark), place optional contact units, ROE weapons hold; emit a
  native find beat (`coalition_in_zone` → message / flag) so success is observe-then-RTB,
  not destroy.
- Validation, planning-options/catalog, golden + Manston example; agent schema/voice learn
  `recon`.
- Acceptance: open compiled recon `.miz` in DCS ME / Instant Action (AOI zone + contacts if
  any; no bomb loadout).

## Non-goals

- Armed recon / bombs / `attack_ground` win conditions; photo-film scoring or camera APIs.
- Free-form LLM Lua; Mist/MOOSE; new trigger condition kinds (reuse zone/mark/message).
- Air opposition bounce on recon v1; multi-theatre; non-Spitfire recon types.
- Full narrative pack parity with CAP/GA (optional later); destroy / group_life_less wins.
- Treating recon as a GA variant with empty payload (rejected — wrong tasking + objectives).

## Capabilities

### New Capabilities

- *(none — extend existing mission-spec / compiler / validation / options / agent)*

### Modified Capabilities

- `mission-spec`: `recon` type; nested `recon` block; `recon_area` objective; contact rules.
- `miz-compiler`: Compile recon Spec (Reconnaissance + AOI zone/mark + optional contacts).
- `mission-validation`: Validate recon geometry/contacts; reject payload/strike/attack.
- `golden-fixtures`: Recon structural golden beside GA / CAP / escort examples.
- `mission-options`: `mission_type` / `recon` as `supported`.
- `nl-agent` / `squadron-voice` / `agent-tools` (light): allow/list/schema/brief for recon.

## Impact

- `models.py`, `validation.py`, `pydcs_compiler.py`, planning_options, agent schema/voice,
  examples, goldens, BACKLOG `#15a`.
- Acceptance: Instant Action / ME smoke of `examples/manston_recon.yaml` → `.miz` with
  Reconnaissance task, AOI zone, no bomb CLSIDs.
