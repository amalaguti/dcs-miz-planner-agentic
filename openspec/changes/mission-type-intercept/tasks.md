## 1. Spec and validation

- [x] 1.1 Extend Mission Spec models for `intercept` mission type, typed enemies, and minimal intercept objective; keep free_flight empty-extension rules
- [x] 1.2 Extend `validate_mission_spec` for intercept (registry aircraft, install theatre); refuse non-empty triggers; keep free_flight refusals
- [x] 1.3 Add checked-in intercept example YAML (Manston Spitfire, Bf-109K-4 enemies, early start, Channel)

## 2. Compiler and fixtures

- [x] 2.1 Compile intercept: place player + enemy flight with registry radios; document enemy spawn coord source; reuse payload-scan workaround
- [x] 2.2 Add intercept golden fixtures + refresh helper path; tests hermetic with injected inventory
- [x] 2.3 Confirm free-flight Manston golden and round-trip tests still pass; Ruff clean; full pytest green

## 3. Docs and acceptance

- [x] 3.1 Update README / ARCHITECTURE / BACKLOG (`building` → `done` on accept); note spawn/radio lessons if non-obvious
- [x] 3.2 Validate + compile intercept example; open `.miz` in DCS Mission Editor / Instant Action (accepted 2026-07-26: ThirdReich/red, 6/6/1944 06:00, Average skill)
