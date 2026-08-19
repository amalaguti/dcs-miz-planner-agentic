## ADDED Requirements

### Requirement: Compiler emits Spitfire Channel radio presets
When compiling a flight whose aircraft is `SpitfireLFMkIX` or
`SpitfireLFMkIXCW`, the compiler SHALL write unit `Radio[1].channels` from the
registry Channel bank (124 / 40 / 41 / 42 / 108.9) on every unit in that
group, including AI mates. Group `frequency` MUST remain 124 MHz. The compiler
MUST NOT use PyDCS `set_frequency()` for this (it sets `radioSet` true).
`radioSet` MUST remain false, matching stock Channel missions. Aircraft
without a packaged channel bank MUST keep frequency-only emit.

#### Scenario: Manston Spitfire A–E match Channel Instant Action
- **WHEN** a Manston cold free-flight Spec with `SpitfireLFMkIX` is compiled
- **THEN** the player unit Radio channels MUST be 124, 40, 41, 42, 108.9,
  group frequency MUST be 124.0, and `radioSet` MUST be false

#### Scenario: Non-Spitfire keeps frequency only
- **WHEN** compiling a P-51D or Bf-109K-4 flight
- **THEN** the compiler MUST NOT write the Spitfire Channel A–E bank onto
  that group
