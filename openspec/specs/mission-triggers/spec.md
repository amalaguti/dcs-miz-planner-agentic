# Mission Triggers

## Purpose

Typed, Lua-free zones and condition→action rules on the Mission Spec. Native `.miz`
trigger emit is a separate compiler change (`trigger-compiler-native`).

## Requirements

### Requirement: Typed zones on Mission Spec
The Mission Spec MAY include a top-level `zones` list. Each zone MUST have a unique `name`,
airfield-relative `bearing_deg` (0–360), `distance_km` (> 0), and `radius_m` (> 0). Absolute
DCS map coordinates MUST NOT be required in v1. Empty `zones` MUST remain valid.

#### Scenario: Relative zone accepted
- **WHEN** a Spec declares a zone with name `patrol`, bearing 135, distance_km 25, radius_m 5000
- **THEN** loading MUST succeed when the rest of the Spec is valid

#### Scenario: Duplicate zone names rejected
- **WHEN** two zones share the same `name`
- **THEN** load or validation MUST fail with a clear error

### Requirement: Typed trigger rules without Lua
The Mission Spec MAY include a top-level `triggers` list of typed rules. Each rule MUST
include a non-empty `when` list (AND of conditions) and a non-empty `then` list of actions.
Rules MUST NOT contain Lua, Mist, MOOSE, or free-form script fields. Optional `name` and
`once` (default true) MAY be present.

#### Scenario: Message after time accepted
- **WHEN** a Spec has a trigger with `when: [{type: time_more, seconds: 60}]` and
  `then: [{type: message, text: "Push."}]`
- **THEN** structural load MUST succeed

#### Scenario: Script field rejected
- **WHEN** a trigger action or condition includes an undeclared field such as `lua` or `script`
- **THEN** loading MUST fail (unknown field)

### Requirement: v1 condition and action vocabulary
Supported condition types MUST include `time_more`, `flag_is`, `unit_dead`, and
`coalition_in_zone`. Supported action types MUST include `message`, `set_flag`, and
`mission_end`. Unknown `type` values MUST be rejected.

#### Scenario: Unknown condition type fails
- **WHEN** a condition uses `type: something_else`
- **THEN** load or validation MUST fail identifying the unknown type

#### Scenario: mission_end win/lose
- **WHEN** an action uses `type: mission_end` with `result: win` or `result: lose`
- **THEN** the Spec MUST accept that action structurally

### Requirement: Trigger and zone reference validation
The shared validation engine SHALL validate trigger/zone graphs: every `coalition_in_zone`
zone name MUST exist in `zones`; every `unit_dead.enemy_index` MUST be in range for
`enemies`; flag names on `flag_is` / `set_flag` MUST be non-empty. Well-formed non-empty
`triggers`/`zones` MUST pass validation (compile may still refuse until native emit exists).

#### Scenario: Missing zone reference fails
- **WHEN** a condition references zone `alpha` but `zones` has no such name
- **THEN** validation MUST fail with a clear missing-zone error

#### Scenario: Valid trigger graph passes validate
- **WHEN** a Spec with a consistent zone and `coalition_in_zone` / `message` trigger is
  validated
- **THEN** validation MUST succeed for the trigger/zone rules
