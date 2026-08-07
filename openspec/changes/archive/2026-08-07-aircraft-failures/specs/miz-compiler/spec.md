## ADDED Requirements

### Requirement: Compiler emits Failures panel table
For each Spec `failures` entry, the compiler SHALL write a mission-root Failures
panel row (`mission.failures`) with `enable` true, `id`, `prob` from `probability`,
After time from `start_after_s` floored to minutes (`hh`/`mm`), and Within minutes
`mmint` from `random_pause_s` using `max(1, ceil(seconds/60))` (Within 0 MUST NOT
be emitted — it never fires). No Lua and no `a_set_failure` triggers MUST be emitted
for this feature. When `failures` is omitted or empty, the compiler MUST NOT add
enabled failure rows from this feature.

#### Scenario: Magneto at T+120
- **WHEN** compiling a Spec with one failure id `ENG0_MAGNETO0` and
  `start_after_s: 120`
- **THEN** the `.miz` MUST contain an enabled `ENG0_MAGNETO0` Failures table entry
  with After 0 hours / 2 minutes and Within at least 1 minute
