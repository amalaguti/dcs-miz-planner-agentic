## ADDED Requirements

### Requirement: Emit set_flag_random
The trigger compiler MUST map Spec `set_flag_random` to PyDCS `SetFlagRandom`
using the shared flag-id mapping, with Spec `min`/`max` as `min_value`/`max_value`.

#### Scenario: Random flag action compiles
- **WHEN** a trigger action is `set_flag_random` with flag `raid`, min `1`, max `4`
- **THEN** the emitted action MUST be Set Flag Random for that flag's numeric id
  with min_value 1 and max_value 4
