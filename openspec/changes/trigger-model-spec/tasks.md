## 1. Models

- [x] 1.1 Add zone + discriminated condition/action + `TriggerRule` Pydantic models (`extra=forbid`)
- [x] 1.2 Change `MissionSpec.triggers` to `list[TriggerRule]`; add `zones: list[TriggerZone]`
- [x] 1.3 Remove blanket “triggers must be empty” model validator; keep combat-type rules

## 2. Validation and compile guard

- [x] 2.1 Validate duplicate zone names, zone refs, `enemy_index` bounds, non-empty when/then
- [x] 2.2 Compiler: refuse non-empty `triggers` or `zones` with clear `#21` message; empty still compiles
- [x] 2.3 Update mission-type tests that asserted “non-empty triggers refused” to typed expectations

## 3. Agent + examples + docs

- [x] 3.1 Update `spec_schema` / prompts with v1 trigger vocabulary and compile-deferred note
- [x] 3.2 Add a validate-only example or test fixture Spec with a simple time→message trigger
- [x] 3.3 Update BACKLOG (`building`/`done` as appropriate), README, ARCHITECTURE briefly

## 4. Verify

- [x] 4.1 pytest green (including compile of existing empty-trigger examples)
- [x] 4.2 Confirm compile of trigger fixture fails with expected message (no `.miz` written)
  - Accepted 2026-08-02: Spec/validate path; compile correctly blocked until `#21`.
    Example: `examples/manston_freeflight_trigger_sample.yaml`
