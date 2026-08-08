## 1. Spec model and validation

- [x] 1.1 Extend `GroundTarget` with optional `motion` (`static` | `patrol` |
      `path`), `patrol_radius_m`, and `path[]` airfield-relative points; pydantic
      rules for mutual exclusion / ranges
- [x] 1.2 Validation: reject bad motion shapes; domain-check path points and
      patrol center vs unit land|sea (reuse channel_domain helpers)
- [x] 1.3 Unit tests for static omit, patrol, path, and domain mismatch rejects

## 2. Compiler

- [x] 2.1 Spike: confirm PyDCS ship + vehicle `add_waypoint` loop emits multi-point
      routes in `.miz` (sea + land)
- [x] 2.2 Implement motion emit in `_apply_ground_attack` and `_apply_recon`
      (patrol polygon + path loop; curated speeds; static unchanged)
- [x] 2.3 Compile tests: U-boat patrol and truck path produce route evidence;
      omit motion matches prior placement behaviour

## 3. Examples, agent, docs

- [x] 3.1 Update `manston_uboat_recon.yaml` + `manston_uboat_hunt.yaml` with
      `motion: patrol` (sea-safe radius)
- [x] 3.2 Add soft-vehicle path example (e.g. `manston_ground_attack_convoy.yaml`)
- [x] 3.3 Planning options + prompts/schema/voice: under-way vs static heuristics;
      brief language when motion present
- [x] 3.4 Update README / ARCHITECTURE / BACKLOG `#15g` building→done on accept;
      LESSONS if waypoint/domain pitfall is non-obvious
- [x] 3.5 Ruff + full pytest green
- [x] 3.6 In-game accept: ME / Instant Action — moving U-boat on water; moving
      truck path inland; static Specs still parked
      (accepted ME 2026-08-08: convoy trucks moving Off Road + Disperse Under Fire
      on WP options; U-boat patrol Specs; airborne disperse smoke deferred to do-soon)
