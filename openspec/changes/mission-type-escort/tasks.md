## 1. Registry, Spec models, and validation

- [x] 1.1 Add `MosquitoFBMkVI` to Channel `aircraft.yaml` with Allied VHF radio (~124.0); confirm exact PyDCS plane id
- [x] 1.2 Add `MissionType.ESCORT`, `ObjectiveType.ESCORT_PACKAGE`, nested `Escort` model (`bearing_deg`, `distance_km`, `altitude_m`, `engagement`), `PackageFlight` (or equivalent) + top-level `package` list; validators require escort + same-coalition package + escort_package; forbid escort/package misuse on other types; keep free_flight / intercept / CAP / ground_attack rules; no strike/targets/payload on escort
- [x] 1.3 Extend shared `validate_mission_spec` for escort registry checks (package + optional enemy aircraft ids; friendly package coalition; opposing enemies)
- [x] 1.4 Unit tests for escort load/validate matrix (happy path, unknown package aircraft, enemy package refused, free_flight+escort refused, strike/payload refused on escort)

## 2. Compiler and example

- [x] 2.1 Implement escort compile path: place friendly package inflight with route to airfield-relative destination; set player Escort task + EscortTaskAction(group_id); apply OptROE from engagement; place optional bounce near destination neighbourhood; choose package main task (CAS vs Ground Attack) during apply
- [x] 2.2 Add `examples/manston_escort.yaml` (Mosquito package + optional Bf-109 bounce); ensure prior mission types compile unchanged
- [x] 2.3 Compiler/unit tests asserting Escort task, EscortTaskAction/groupId, package aircraft, and optional enemies in emitted mission structure

## 3. Options, catalog, agent, voice

- [x] 3.1 Add `mission_type`/`escort` to `planning_options.yaml` as supported
- [x] 3.2 Catalog sync / `list_mission_options` tests include `escort`
- [x] 3.3 Update agent planning rules allow-list + `get_mission_spec_schema` for `escort` (example + notes; airfield-relative destination; no invented coords/ids)
- [x] 3.4 Add escort branch to `build_commander_brief` (tactics/procedures/watch-outs: stay with package, ROE, bounce)

## 4. Goldens, docs, acceptance

- [x] 4.1 Add escort golden fixtures + refresh helper; hermetic pytest regression
- [x] 4.2 Update README / ARCHITECTURE / BACKLOG (`mission-type-escort` building→done when accepted); LESSONS for EscortTaskAction / package placement / bounce offset if non-obvious
- [x] 4.3 Ruff + full pytest green
- [x] 4.4 In-game accept: open compiled escort `.miz` in DCS ME / Instant Action; confirm package route and Escort tasking; note result in tasks/LESSONS
  - Accepted 2026-08-02: `out/manston_escort.miz` — Mosquito package + Escort tasking + bounce played well in DCS
