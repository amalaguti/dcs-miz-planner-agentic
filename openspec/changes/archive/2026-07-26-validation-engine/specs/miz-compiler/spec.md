## ADDED Requirements

### Requirement: Compile uses shared validation engine
Before creating a `.miz`, the free-flight compiler SHALL run the shared Mission Spec validation
engine. If validation fails, compilation MUST NOT write a `.miz` and MUST surface the validation
errors (or an equivalent clear aggregate error) without inventing a second, divergent rule set for
registry/airfield/theatre checks.

#### Scenario: Invalid Spec does not produce a .miz
- **WHEN** a Mission Spec fails shared validation (for example unknown airfield)
- **THEN** the compiler MUST NOT write an output `.miz` file and MUST report the validation failure

#### Scenario: Valid Manston Spec still compiles
- **WHEN** the checked-in Manston free-flight Mission Spec passes shared validation
- **THEN** the compiler MUST still produce a `.miz` that places the player cold at Manston with
  Spitfire group frequency 124.0 MHz and remains openable in DCS Mission Editor / Instant Action
