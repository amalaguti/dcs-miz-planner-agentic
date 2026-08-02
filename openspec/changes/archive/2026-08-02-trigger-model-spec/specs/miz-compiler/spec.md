## ADDED Requirements

### Requirement: Compile refuses undeclared trigger emit
Until native trigger compilation is implemented, the compiler MUST refuse to write a `.miz`
when the Mission Spec has a non-empty `triggers` list or a non-empty `zones` list. The
error MUST state that trigger/zone emit is not available yet. Specs with empty `triggers`
and empty `zones` MUST continue to compile as today.

#### Scenario: Empty triggers still compile
- **WHEN** the checked-in Manston cold free-flight Spec (empty triggers/zones) is compiled
- **THEN** the compiler MUST write a `.miz` successfully

#### Scenario: Non-empty triggers blocked at compile
- **WHEN** a Spec that validates with a non-empty `triggers` list is compiled
- **THEN** the compiler MUST fail without writing a `.miz`, with a clear not-implemented
  message
