## ADDED Requirements

### Requirement: Compile emits native zones and triggers
When a Mission Spec has non-empty `zones` or `triggers`, the compiler SHALL write
corresponding native DCS trigger zones and trigger rules into the `.miz` via PyDCS (or
equivalent). It MUST NOT refuse solely because triggers are present. Specs with empty
zones and triggers MUST keep prior compile behaviour.

#### Scenario: Time message sample compiles
- **WHEN** `examples/manston_freeflight_trigger_sample.yaml` is compiled
- **THEN** the `.miz` MUST contain a time-after condition and an out-text (message) action
  and MUST still place the player cold at Manston

#### Scenario: Empty triggers still compile
- **WHEN** the Manston cold free-flight Spec (empty triggers) is compiled
- **THEN** prior free-flight behaviour MUST remain

### Requirement: Spec vocabulary maps to ME predicates
The compiler SHALL map v1 Spec conditions/actions to native predicates: `time_more` to
time-after, `flag_is` to flag true/false, `unit_dead` to group-dead for the referenced
enemy flight, `coalition_in_zone` to part-of-coalition-in-zone; `message` to delayed
out-text, `set_flag` to set/clear flag, `mission_end` to end-mission with win/lose for the
player coalition. Unsupported types MUST fail clearly before writing a `.miz`.

#### Scenario: Unknown mapping fails
- **WHEN** a future/unsupported condition type somehow reaches compile
- **THEN** compile MUST fail with a clear error and MUST NOT write a `.miz`
