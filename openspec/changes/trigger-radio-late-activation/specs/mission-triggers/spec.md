## ADDED Requirements

### Requirement: Radio menu actions
The Mission Spec trigger action vocabulary MUST include `radio_item_add` and
`radio_item_remove`. `radio_item_add` MUST accept a non-empty `label`, a non-empty string
`flag` name, and MAY accept an optional `coalition`. When coalition is set, the compiler
MUST emit a coalition-scoped F10 radio item that sets that flag on (ME value 1). When
omitted, the compiler MUST emit an all-players radio item with the same flag behaviour.
`radio_item_remove` MUST accept a `label` matching a previously added item. Actions MUST
NOT accept free-form Lua.

#### Scenario: Radio add accepted structurally
- **WHEN** a trigger action uses `type: radio_item_add` with `label` and `flag`
- **THEN** structural load MUST succeed

#### Scenario: Radio remove accepted structurally
- **WHEN** a trigger action uses `type: radio_item_remove` with `label`
- **THEN** structural load MUST succeed

### Requirement: Activate and deactivate group actions
The Mission Spec trigger action vocabulary MUST include `activate_group` and
`deactivate_group`. Each MUST reference exactly one of `enemy_index` or `target_index`
(0-based). Validation MUST reject out-of-range indices and MUST reject actions that set
neither or both indices. The compiler MUST map the index to the corresponding placed
group id.

#### Scenario: Activate enemy by index
- **WHEN** an action uses `type: activate_group` with `enemy_index: 0` and `enemies` is
  non-empty
- **THEN** validation MUST succeed for that reference and compile MUST emit group activate
  for that enemy group

#### Scenario: Missing index fails
- **WHEN** `activate_group` omits both `enemy_index` and `target_index`
- **THEN** load or validation MUST fail clearly

## MODIFIED Requirements

### Requirement: v1 condition and action vocabulary
Supported condition types MUST include `time_more`, `flag_is`, `unit_dead`,
`coalition_in_zone`, and `target_dead`. Supported action types MUST include `message`,
`set_flag`, `mission_end`, `radio_item_add`, `radio_item_remove`, `activate_group`, and
`deactivate_group`. Unknown `type` values MUST be rejected.

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
