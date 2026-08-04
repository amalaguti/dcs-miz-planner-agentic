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

### Requirement: Validated triggers are compileable
A Spec that passes shared validation for typed zones/triggers MUST be accepted by the
compiler for native emit (subject to registry/install checks). The system MUST NOT leave
validated trigger graphs as validate-only once native compile is implemented.

#### Scenario: Valid sample is not refused
- **WHEN** the checked-in free-flight trigger sample validates successfully
- **THEN** compile MUST proceed to write a `.miz` (not a not-implemented refusal)

### Requirement: Narrative-produced rules stay in v1 vocabulary
Zones and triggers produced by narrative expansion MUST use only supported v1 condition
types (`time_more`, `flag_is`, `flag_equals`, `flag_more`, `flag_less`,
`time_since_flag`, `unit_dead`, `coalition_in_zone`, `target_dead`) and action types
(`message`, `set_flag`, `set_flag_value`, `inc_flag`, `mission_end`, `sound`,
`radio_item_add`, `radio_item_remove`, `activate_group`, `deactivate_group`). They MUST
remain eligible for native ME compile emit without Lua. Narrative packs MUST NOT be
required to emit sound or numeric-flag rules.

#### Scenario: Expanded CAP graph validates
- **WHEN** a CAP Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met

#### Scenario: Expanded ground-attack graph validates
- **WHEN** a ground_attack Spec with `narrative.enabled: true` is expanded and validated
- **THEN** validation MUST succeed for the resulting zone/trigger graph when pack
  preconditions are met
