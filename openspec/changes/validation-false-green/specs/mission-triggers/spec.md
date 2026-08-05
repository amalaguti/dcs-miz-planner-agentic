## MODIFIED Requirements

### Requirement: Activate and deactivate group actions
The Mission Spec trigger action vocabulary MUST include `activate_group` and
`deactivate_group`. Each MUST reference exactly one of `enemy_index` or `target_index`
(0-based). Validation MUST reject out-of-range indices and MUST reject actions that set
neither or both indices. Validation MUST also reject activate/deactivate actions whose
referenced enemy or target does not have `late_activation: true`, and MUST reject Specs
where a late-activated enemy or target has no corresponding `activate_group`. The compiler
MUST map the index to the corresponding placed group id.

#### Scenario: Activate enemy by index
- **WHEN** an action uses `type: activate_group` with `enemy_index: 0`, that enemy has
  `late_activation: true`, and `enemies` is non-empty
- **THEN** validation MUST succeed for that reference and compile MUST emit group activate
  for that enemy group

#### Scenario: Missing index fails
- **WHEN** `activate_group` omits both `enemy_index` and `target_index`
- **THEN** load or validation MUST fail clearly

#### Scenario: Activate without late_activation fails
- **WHEN** `activate_group` references an enemy with `late_activation` false or omitted
- **THEN** validation MUST fail clearly

## ADDED Requirements

### Requirement: Message delay_s must be zero until implemented
Message actions MAY include `delay_s` only as zero (or omit the field). Non-zero
`delay_s` MUST be rejected at load or validation. Timing of messages MUST be expressed
via trigger conditions until the compiler implements delayed message emit.

#### Scenario: Non-zero message delay rejected
- **WHEN** a message action sets `delay_s` greater than zero
- **THEN** load or validation MUST fail clearly
