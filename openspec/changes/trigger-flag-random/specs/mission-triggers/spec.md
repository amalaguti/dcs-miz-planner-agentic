## ADDED Requirements

### Requirement: Spec set_flag_random action
The Mission Spec MUST support a trigger action `set_flag_random` with a named
`flag` and integer `min` / `max` bounds. Validation MUST reject `min > max`.

#### Scenario: Valid random flag action loads
- **WHEN** a Spec trigger `then` includes `set_flag_random` with `min` ≤ `max`
- **THEN** the Spec MUST load and validate successfully

#### Scenario: Inverted range rejected
- **WHEN** `min` is greater than `max`
- **THEN** validation MUST fail with a clear error

### Requirement: Compiler emits Set Flag Random
Compiling a Spec that uses `set_flag_random` MUST emit ME action
`a_set_flag_random` (via PyDCS `SetFlagRandom`) for the mapped flag id.

#### Scenario: Compile includes a_set_flag_random
- **WHEN** a Spec with `set_flag_random` is compiled
- **THEN** the `.miz` mission table MUST contain `a_set_flag_random`
