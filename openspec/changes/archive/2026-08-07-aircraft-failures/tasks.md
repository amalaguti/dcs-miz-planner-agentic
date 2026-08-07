## 1. Catalog + Spec model

- [x] 1.1 Add `data/channel/aircraft_failures.yaml` curated SpitfireLFMkIX ids + labels
- [x] 1.2 Registry API: list/lookup failures by aircraft
- [x] 1.3 Spec models: `FailureEvent` + optional `MissionSpec.failures`
- [x] 1.4 Validation: unknown id / ranges / aircraft without catalog

## 2. Compiler emit

- [x] 2.1 Emit ME Failures panel rows (`enable`/`hh`/`mm`/`mmint`/`prob`) per entry
- [x] 2.2 Empty/omit failures → no enabled failure rows / no `a_set_failure`
- [x] 2.3 Compile smoke + structural asserts (id + enabled Failures table)

## 3. Example, options, agent surfaces

- [x] 3.1 Example Spec (e.g. Manston free-flight magneto at T+120)
- [x] 3.2 Planning-options entries; schema notes; brief/voice honesty
- [x] 3.3 Unit tests for validate reject + compile

## 4. Docs + acceptance

- [x] 4.1 BACKLOG `#22b` → building/done; LESSONS if ME id quirks; README if needed
- [x] 4.2 In-game ME: Set Failure visible; optional Instant Action magneto smoke
  - Accepted 2026-08-07: Mag 1 Failures panel (After 0:02 / Within 1) cuts with Mag 2 OFF; messages OK. Within=0 / `a_set_failure` path abandoned for Failures table.
