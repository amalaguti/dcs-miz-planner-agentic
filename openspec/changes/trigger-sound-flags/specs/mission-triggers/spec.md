## ADDED Requirements

### Requirement: Sound action with curated asset id
The Mission Spec trigger action vocabulary MUST include `sound`. A `sound` action MUST
accept a non-empty string `asset_id` that names an entry in the product sound-asset
registry. The Spec MUST NOT accept arbitrary filesystem paths, URLs, or embedded binary
payloads for sound. Actions MUST NOT accept free-form Lua.

#### Scenario: Sound action accepted structurally
- **WHEN** a trigger action uses `type: sound` with a known registry `asset_id`
- **THEN** structural load MUST succeed

#### Scenario: Path-like sound field rejected
- **WHEN** a sound action includes an undeclared path field (e.g. `file` or `path`)
- **THEN** loading MUST fail (unknown field)

### Requirement: Numeric and timed flag conditions
The Mission Spec trigger condition vocabulary MUST include `flag_equals`, `flag_more`,
`flag_less`, and `time_since_flag`. Each MUST accept a non-empty string `flag` name.
`flag_equals` / `flag_more` / `flag_less` MUST accept an integer `value`.
`time_since_flag` MUST accept `seconds` (> 0). Existing `flag_is` bool semantics MUST
remain unchanged.

#### Scenario: flag_equals accepted
- **WHEN** a condition uses `type: flag_equals` with `flag` and `value: 3`
- **THEN** structural load MUST succeed

#### Scenario: time_since_flag accepted
- **WHEN** a condition uses `type: time_since_flag` with `flag` and `seconds: 30`
- **THEN** structural load MUST succeed

### Requirement: Numeric flag actions
The Mission Spec trigger action vocabulary MUST include `inc_flag` and `set_flag_value`.
Both MUST accept a non-empty string `flag` name. `set_flag_value` MUST accept an integer
`value`. `inc_flag` MAY accept an integer `by` (default 1). Existing `set_flag` bool
semantics MUST remain unchanged.

#### Scenario: inc_flag accepted
- **WHEN** an action uses `type: inc_flag` with `flag` and optional `by`
- **THEN** structural load MUST succeed

#### Scenario: set_flag_value accepted
- **WHEN** an action uses `type: set_flag_value` with `flag` and `value: 0`
- **THEN** structural load MUST succeed

## MODIFIED Requirements

### Requirement: v1 condition and action vocabulary
Supported condition types MUST include `time_more`, `flag_is`, `flag_equals`,
`flag_more`, `flag_less`, `time_since_flag`, `unit_dead`, `coalition_in_zone`, and
`target_dead`. Supported action types MUST include `message`, `set_flag`,
`set_flag_value`, `inc_flag`, `mission_end`, `sound`, `radio_item_add`,
`radio_item_remove`, `activate_group`, and `deactivate_group`. Unknown `type` values
MUST be rejected.

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

### Requirement: Trigger and zone reference validation
The shared validation engine SHALL validate trigger/zone graphs: every `coalition_in_zone`
zone name MUST exist in `zones`; every `unit_dead.enemy_index` MUST be in range for
`enemies`; every `target_dead.target_index` MUST be in range for `targets`; flag names on
`flag_is` / `flag_equals` / `flag_more` / `flag_less` / `time_since_flag` / `set_flag` /
`set_flag_value` / `inc_flag` MUST be non-empty; every `sound.asset_id` MUST exist in the
product sound-asset registry. Well-formed non-empty `triggers`/`zones` MUST pass
validation and MUST be eligible for native compile emit.

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

#### Scenario: Unknown sound asset_id fails
- **WHEN** a `sound` action uses `asset_id` not present in the registry
- **THEN** validation MUST fail with a clear unknown-asset error

### Requirement: Narrative-produced rules stay in v1 vocabulary
Zones and triggers produced by narrative expansion MUST use only supported v1 condition
types (`time_more`, `flag_is`, `flag_equals`, `flag_more`, `flag_less`,
`time_since_flag`, `unit_dead`, `coalition_in_zone`, `target_dead`) and action types
(`message`, `set_flag`, `set_flag_value`, `inc_flag`, `mission_end`, `sound`,
`radio_item_add`, `radio_item_remove`, `activate_group`, `deactivate_group`). They MUST
remain eligible for native ME compile emit without Lua. Narrative packs MUST NOT be
required to emit sound or numeric-flag rules in this change.

#### Scenario: Expanded CAP graph validates
- **WHEN** a CAP Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met

#### Scenario: Expanded ground-attack graph validates
- **WHEN** a ground_attack Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met
