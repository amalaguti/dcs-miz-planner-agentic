## 1. Spec model and validation

- [x] 1.1 Add `MissionType.RECON`, `ObjectiveType.RECON_AREA`, nested `Recon` model
      (`bearing_deg`, `distance_km`, `altitude_m`, `radius_m` with default, optional `mark`);
      require `recon` + `recon_area`; forbid payload / strike / cap / escort / non-empty
      enemies; optional opposing-coalition `targets`; forbid `recon` on other types
- [x] 1.2 Extend `validate_mission_spec` for recon (geometry bounds, contact unit registry,
      opposing coalition, no payload)
- [x] 1.3 Unit tests: happy path, empty targets, same-coalition contact refused, payload
      refused, free_flight+recon refused, attack_ground on recon refused

## 2. Compiler and example

- [x] 2.1 Implement recon compile path: `Reconnaissance` task, ingress to AOI, AOI zone
      (+ optional mark), OptROE weapons hold, place optional contacts without attack
      tasking, emit find beat (`coalition_in_zone` → message + reserved flag ≥830)
- [x] 2.2 Add `examples/manston_recon.yaml` (Manston AOI + soft truck contacts; no payload)
- [x] 2.3 Compiler/unit tests asserting Reconnaissance task, AOI zone, no bomb CLSIDs,
      contacts, find-message/trigger text

## 3. Options, catalog, agent, voice

- [x] 3.1 Add `mission_type`/`recon` to `planning_options.yaml` as supported
- [x] 3.2 Catalog sync / `list_mission_options` includes `recon`
- [x] 3.3 Update agent allow-list + `get_mission_spec_schema` for recon (no payload;
      observe-only contacts)
- [x] 3.4 Add recon branch to `build_commander_brief` (observe / RTB; not bomb run)

## 4. Goldens, docs, acceptance

- [x] 4.1 Add recon golden fixtures + hermetic pytest regression
- [x] 4.2 Update README / ARCHITECTURE / BACKLOG `#15a` building→done when accepted;
      LESSONS + `dcs-dev-*` only if non-obvious PyDCS/AOI pitfalls
- [x] 4.3 Ruff + full pytest green
- [x] 4.4 In-game accept: open compiled recon `.miz` in DCS ME / Instant Action; confirm
      Reconnaissance + AOI zone (+ contacts); note result in tasks
      (Accepted 2026-08-07: ME triggers/zone + Reconnaissance OK.)
