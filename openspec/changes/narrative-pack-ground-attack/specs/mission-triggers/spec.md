## MODIFIED Requirements

### Requirement: v1 condition and action vocabulary
Supported condition types MUST include `time_more`, `flag_is`, `unit_dead`,
`coalition_in_zone`, and `target_dead`. Supported action types MUST include `message`,
`set_flag`, and `mission_end`. Unknown `type` values MUST be rejected.

#### Scenario: Unknown condition type fails
- **WHEN** a condition uses `type: something_else`
- **THEN** load or validation MUST fail identifying the unknown type

#### Scenario: mission_end win/lose
- **WHEN** an action uses `type: mission_end` with `result: win` or `result: lose`
- **THEN** the Spec MUST accept that action structurally

#### Scenario: target_dead accepted
- **WHEN** a condition uses `type: target_dead` with `target_index: 0`
- **THEN** structural load MUST succeed

### Requirement: Trigger and zone reference validation
The shared validation engine SHALL validate trigger/zone graphs: every `coalition_in_zone`
zone name MUST exist in `zones`; every `unit_dead.enemy_index` MUST be in range for
`enemies`; every `target_dead.target_index` MUST be in range for `targets`; flag names on
`flag_is` / `set_flag` MUST be non-empty. Well-formed non-empty `triggers`/`zones` MUST
pass validation and MUST be eligible for native compile emit.

#### Scenario: Missing zone reference fails
- **WHEN** a condition references zone `alpha` but `zones` has no such name
- **THEN** validation MUST fail with a clear missing-zone error

#### Scenario: Valid trigger graph passes validate
- **WHEN** a Spec with a consistent zone and `coalition_in_zone` / `message` trigger is
  validated
- **THEN** validation MUST succeed for the trigger/zone rules

#### Scenario: Out-of-range target_dead fails
- **WHEN** `target_dead.target_index` is 0 but `targets` is empty
- **THEN** validation MUST fail with a clear error

### Requirement: Narrative-produced rules stay in v1 vocabulary
Zones and triggers produced by narrative expansion MUST use only supported v1 condition
types (`time_more`, `flag_is`, `unit_dead`, `coalition_in_zone`, `target_dead`) and action
types (`message`, `set_flag`, `mission_end`). They MUST remain eligible for native ME
compile emit without Lua.

#### Scenario: Expanded CAP graph validates
- **WHEN** a CAP Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met

#### Scenario: Expanded ground-attack graph validates
- **WHEN** a ground_attack Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met
