## 1. Validation API

- [x] 1.1 Add `ValidationError` / `ValidationResult` / `MissionValidationError` types (path, code, message, optional hint)
- [x] 1.2 Implement `validate_mission_spec(spec, *, registry=..., inventory=...)` collecting registry + install + free-flight semantic errors
- [x] 1.3 Theatre checks: registry support AND install inventory `available` + `planner_supported`; clear diagnostic when inventory unusable
- [x] 1.4 Aircraft, weather preset, and airfield DCS-exists checks via Channel registry with known-value hints

## 2. CLI and compiler wiring

- [x] 2.1 Add `dcs-miz validate <spec.yaml> [--json]` (exit 0 ok, 2 on load/validate failure)
- [x] 2.2 Replace compiler-local registry `_validate` with shared engine; do not write `.miz` on failure
- [x] 2.3 Preserve legacy compile, `compile` subcommand, and `theatres` behavior

## 3. Tests

- [x] 3.1 Unit tests: Manston passes with injected available Channel inventory; unknown airfield/aircraft/weather; multiple errors; theatre not available locally
- [x] 3.2 CLI validate success/failure tests; compile refuses invalid Spec without writing output
- [x] 3.3 Existing Manston compile + schema/registry/install tests still pass; Ruff clean

## 4. Docs and acceptance

- [x] 4.1 Update README, `docs/ARCHITECTURE.md`, `docs/BACKLOG.md` (item `building` → done on accept)
- [x] 4.2 Run `dcs-miz validate` on Manston example with real/local inventory; confirm ok
- [x] 4.3 Compile Manston after validate path; open `.miz` in DCS Mission Editor / Instant Action (accepted 2026-07-26: load perfect)
