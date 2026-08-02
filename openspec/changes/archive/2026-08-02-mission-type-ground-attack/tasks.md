## 1. Registry, Spec models, and validation

- [x] 1.1 Add `payloads.yaml` presets (`spitfire_2x250_slipper` default Channel-crossing, `spitfire_2x250`, `spitfire_1x500`) with verified SpitfireLFMkIX pylon/CLSID pairs (note centreline tank vs 500 lb exclusivity); add `ground_units.yaml` with a small verified WWII enemy set (e.g. `Blitz_36-6700A`, `flak18`); extend registry API for payload + ground-unit lookup
- [x] 1.2 Add `MissionType.GROUND_ATTACK`, `ObjectiveType.ATTACK_GROUND`, nested `Strike` model, `GroundTarget` model, optional `player.payload`; validators require strike + enemy-only targets (opposing coalition) + payload + attack_ground; forbid strike/payload/targets misuse on other types; keep free_flight / intercept / CAP rules
- [x] 1.3 Extend shared `validate_mission_spec` for ground-attack registry/install checks (payload aircraft match, ground unit ids, empty air enemies, reject same-coalition targets)
- [x] 1.4 Unit tests for ground-attack load/validate matrix (happy path, unknown payload/unit, friendly target refused, free_flight+strike refused, enemies forbidden)

## 2. Compiler and example

- [x] 2.1 Implement ground-attack compile path: apply registry pylons after `_disable_payload_scan`, set GroundAttack task, allow tank jettison (do not set OptRestrictJettison; optional OptJettisonEmptyTanks), airfield-relative strike waypoints (+ Bombing or AttackGroup as decided), place enemy ground vehicle groups
- [x] 2.2 Add `examples/manston_ground_attack.yaml` using `spitfire_2x250_slipper`; ensure free-flight / intercept / CAP compile unchanged
- [x] 2.3 Compiler/unit tests asserting GroundAttack task, bomb + slipper CLSIDs, and ground units in emitted mission structure

## 3. Options, catalog, agent, voice

- [x] 3.1 Add `mission_type`/`ground_attack` to `planning_options.yaml`; promote `payload_family` presets to supported/advisory with `meta.payload`
- [x] 3.2 Catalog sync / `list_mission_options` tests include `ground_attack` and non-future payload families
- [x] 3.3 Update agent planning rules allow-list + `get_mission_spec_schema` for `ground_attack` (example + notes; prefer slipper for Channel crossing; no invented CLSIDs/coords)
- [x] 3.4 Add ground-attack branch to `build_commander_brief` (tactics/procedures/watch-outs including jettison tank before attack when slipper present)

## 4. Goldens, docs, acceptance

- [x] 4.1 Add ground-attack golden fixtures + refresh helper; hermetic pytest regression
- [x] 4.2 Update README / ARCHITECTURE / BACKLOG (`mission-type-ground-attack` building→done when accepted); LESSONS for loadout apply / strike math / Bombing vs AttackGroup if non-obvious
- [x] 4.3 Ruff + full pytest green
- [x] 4.4 In-game accept: open compiled ground-attack `.miz` in DCS ME / Instant Action; confirm Target waypoint and units are on land (not mid-Channel); note result in tasks/LESSONS
  - Checklist (every GA mission): PyDCS bearing/distance vs known airports; land vehicles on enemy land (or practice UK-side); water → ships only; ME planner target matches placement
  - Accepted 2026-08-02: `out/manston_ground_attack.miz` — Dunkirk inland strike (~125°/76 km) on land OK in DCS ME
