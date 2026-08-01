## 1. Spec models and validation

- [x] 1.1 Add `MissionType.CAP`, `ObjectiveType.PATROL`, `CapPattern`, `Engagement`, and nested `Cap` model (`bearing_deg`, `distance_km`, `altitude_m`, `pattern`, optional `duration_min`, `engagement`)
- [x] 1.2 Extend `MissionSpec` validators: require `cap` + `patrol` objective for CAP; optional enemies; forbid `cap` on other types; keep free_flight / intercept rules
- [x] 1.3 Extend shared `validate_mission_spec` for CAP registry/install checks (enemies when present)
- [x] 1.4 Unit tests for CAP load/validate matrix (pure patrol, with enemies, bad engagement/pattern, free_flight+cap refused)

## 2. Compiler and example

- [x] 2.1 Implement CAP compile path: group task CAP, airfield-relative station waypoint + Orbit (+ ControlledTask duration when set), OptROE from engagement, race_track second point when needed
- [x] 2.2 Place optional CAP enemies (prefer station-neighbourhood offset; document constants)
- [x] 2.3 Add `examples/manston_cap.yaml` and ensure free-flight / intercept compile unchanged
- [x] 2.4 Compiler/unit tests asserting CAP task, Orbit, ROE option, and optional enemies in emitted mission structure

## 3. Options, catalog, agent, voice

- [x] 3.1 Add `mission_type`/`cap` to `planning_options.yaml`; promote `roe_seed` to supported/advisory with `meta.engagement`
- [x] 3.2 Catalog sync / `list_mission_options` tests include `cap` and non-future ROE
- [x] 3.3 Update agent planning rules allow-list for `cap` + `cap` block shape
- [x] 3.4 Add CAP branch to `build_commander_brief` (tactics/procedures/watch-outs)

## 4. Goldens, docs, acceptance

- [x] 4.1 Add CAP golden fixtures + refresh helper; hermetic pytest regression
- [x] 4.2 Update README / ARCHITECTURE / BACKLOG (`mission-type-cap` building→done when accepted); note briefing waits until M4 types finish; LESSONS for station math / ROE / enemy offset
- [x] 4.3 Ruff + full pytest green
- [x] 4.4 In-game accept: open compiled CAP `.miz` in DCS ME / Instant Action; note result in tasks/LESSONS
  - Accepted 2026-08-01: `out/manston_cap.miz` loaded OK in DCS (ME / Instant Action)
