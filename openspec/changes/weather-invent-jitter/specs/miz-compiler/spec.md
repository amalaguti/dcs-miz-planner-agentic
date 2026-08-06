## ADDED Requirements

### Requirement: Compiler applies invent weather snapshot
Before writing weather into the `.miz`, the compiler MUST apply the invent-
resolved weather snapshot for the Spec (gallery clamp, fog, temp, QNH, turb,
wind layers as present). Given the same Spec including `weather_opts.seed`,
compile MUST be deterministic. Unsupported gallery ids in a snapshot MUST fail
clearly before writing a `.miz`.

#### Scenario: Pinned seed compile stable
- **WHEN** a gallery-pattern Spec with `weather_opts.seed` set is compiled twice
- **THEN** the mission weather table fields covered by the snapshot MUST match
  between runs

#### Scenario: Legacy sunny with seed still compiles
- **WHEN** `sunny_clear` with an explicit seed is compiled
- **THEN** compile MUST succeed without assigning a rainy gallery preset
