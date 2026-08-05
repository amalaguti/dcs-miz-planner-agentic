## ADDED Requirements

### Requirement: Mark action for F10 map marks
The Mission Spec trigger action vocabulary MUST include `mark`. A `mark` action MUST
accept a non-empty `zone` name that references a Spec zone and a non-empty `text` string
for the F10 map mark. It MAY accept `readonly` (boolean, default true). The Spec MUST NOT
accept free-form Lua, raw map coordinates, or author-supplied mark ids.

#### Scenario: Mark action accepted structurally
- **WHEN** a trigger action uses `type: mark` with `zone` and `text`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

#### Scenario: Empty mark text fails
- **WHEN** a `mark` action sets empty `text`
- **THEN** load or validation MUST fail clearly

### Requirement: Smoke action for zone smoke markers
The Mission Spec trigger action vocabulary MUST include `smoke`. A `smoke` action MUST
accept a non-empty `zone` name that references a Spec zone and a `color` from the curated
set `green`, `red`, `white`, `orange`, `blue` (ME Smoke Marker colors). It MAY accept
`altitude_m` (> 0, default 1). Actions MUST NOT accept free-form Lua or arbitrary color
integers from the Spec author.

#### Scenario: Smoke action accepted structurally
- **WHEN** a trigger action uses `type: smoke` with `zone` and `color: red`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

#### Scenario: Invalid smoke color fails
- **WHEN** a `smoke` action sets an unknown `color`
- **THEN** load or validation MUST fail clearly

## MODIFIED Requirements

### Requirement: v1 condition and action vocabulary
Supported condition types MUST include `time_more`, `flag_is`, `flag_equals`,
`flag_more`, `flag_less`, `time_since_flag`, `unit_dead`, `coalition_in_zone`,
`target_dead`, and `group_life_less`. Supported action types MUST include `message`,
`set_flag`, `set_flag_value`, `inc_flag`, `mission_end`, `sound`, `radio_item_add`,
`radio_item_remove`, `activate_group`, `deactivate_group`, `mark`, and `smoke`. Unknown
`type` values MUST be rejected.

#### Scenario: Unknown condition type fails
- **WHEN** a condition uses `type: something_else`
- **THEN** load or validation MUST fail identifying the unknown type

#### Scenario: mission_end win/lose
- **WHEN** an action uses `type: mission_end` with `result: win` or `result: lose`
- **THEN** the Spec MUST accept that action structurally

#### Scenario: target_dead accepted
- **WHEN** a condition uses `type: target_dead` with `target_index: 0`
- **THEN** structural load MUST succeed

#### Scenario: radio_item_add accepted
- **WHEN** a condition uses supported types and an action uses `type: radio_item_add`
- **THEN** structural load MUST succeed when required fields are present

#### Scenario: sound accepted in vocabulary
- **WHEN** an action uses `type: sound` with `asset_id`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

#### Scenario: group_life_less accepted in vocabulary
- **WHEN** a condition uses `type: group_life_less` with a valid index and `percent`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

#### Scenario: mark accepted in vocabulary
- **WHEN** an action uses `type: mark` with `zone` and `text`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

#### Scenario: smoke accepted in vocabulary
- **WHEN** an action uses `type: smoke` with `zone` and a curated `color`
- **THEN** structural load MUST succeed when the rest of the Spec is valid

### Requirement: Trigger and zone reference validation
The shared validation engine SHALL validate trigger/zone graphs: every `coalition_in_zone`
zone name MUST exist in `zones`; every `mark.zone` and `smoke.zone` MUST exist in
`zones`; every `unit_dead.enemy_index` MUST be in range for `enemies`; every
`target_dead.target_index` MUST be in range for `targets`; every `group_life_less` index
MUST be in range for the referenced `enemies` or `targets` list and MUST use exactly one
of `enemy_index` or `target_index`; `group_life_less.percent` MUST be an integer from 1
to 100 inclusive; flag names on `flag_is` / `flag_equals` / `flag_more` / `flag_less` /
`time_since_flag` / `set_flag` / `set_flag_value` / `inc_flag` MUST be non-empty; every
`sound.asset_id` MUST exist in the product sound-asset registry; every `smoke.color` MUST
be one of the curated colors. Well-formed non-empty `triggers`/`zones` MUST pass
validation and MUST be eligible for native compile emit.

#### Scenario: Missing zone reference fails
- **WHEN** a condition references zone `alpha` but `zones` has no such name
- **THEN** validation MUST fail with a clear missing-zone error

#### Scenario: Missing mark zone fails
- **WHEN** a `mark` action references zone `alpha` but `zones` has no such name
- **THEN** validation MUST fail with a clear missing-zone error

#### Scenario: Valid trigger graph passes validate
- **WHEN** a Spec with a consistent zone and `coalition_in_zone` / `message` trigger is
  validated
- **THEN** validation MUST succeed for the trigger/zone rules

#### Scenario: Out-of-range target_dead fails
- **WHEN** `target_dead.target_index` is 0 but `targets` is empty
- **THEN** validation MUST fail with a clear error

#### Scenario: Unknown sound asset_id fails
- **WHEN** a `sound` action uses `asset_id` not present in the registry
- **THEN** validation MUST fail with a clear unknown-asset error

#### Scenario: Out-of-range group_life_less fails
- **WHEN** `group_life_less.target_index` is 0 but `targets` is empty
- **THEN** validation MUST fail with a clear error

### Requirement: Narrative-produced rules stay in v1 vocabulary
Zones and triggers produced by narrative expansion MUST use only supported v1 condition
types (`time_more`, `flag_is`, `flag_equals`, `flag_more`, `flag_less`,
`time_since_flag`, `unit_dead`, `coalition_in_zone`, `target_dead`, `group_life_less`)
and action types (`message`, `set_flag`, `set_flag_value`, `inc_flag`, `mission_end`,
`sound`, `radio_item_add`, `radio_item_remove`, `activate_group`, `deactivate_group`,
`mark`, `smoke`). They MUST remain eligible for native ME compile emit without Lua.
Narrative packs MUST NOT be required to emit `mark` or `smoke` rules in this change.

#### Scenario: Expanded CAP graph validates
- **WHEN** a CAP Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met

#### Scenario: Expanded ground-attack graph validates
- **WHEN** a ground_attack Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met
