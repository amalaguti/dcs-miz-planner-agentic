## 1. Tools package

- [x] 1.1 Create `src/dcs_miz_planner/tools/` with shared structured result helpers (`ok` / error)
- [x] 1.2 Implement `find_airfield` and `get_aircraft_details` against `CatalogService`
- [x] 1.3 Implement `list_mission_options` (catalog enums + offerable theatres)
- [x] 1.4 Implement `validate_mission_spec` and `compile_mission` wrapping existing engines
- [x] 1.5 Export the five tools from a stable `dcs_miz_planner.tools` import surface

## 2. Tests and optional CLI

- [x] 2.1 Pytest: lookup tools (Manston, Spitfire, unknown aircraft); options include free_flight/intercept
- [x] 2.2 Pytest: validate + compile Manston free-flight Spec via tools (temp output)
- [x] 2.3 Optional thin CLI only if it stays minimal; otherwise document API-only acceptance
- [x] 2.4 Ruff clean; full suite green

## 3. Docs and acceptance

- [x] 3.1 Update ARCHITECTURE / README / BACKLOG for tools surface
- [x] 3.2 Acceptance: invoke tools (tests and/or CLI) for catalog lookups + validate/compile on checked-in example
