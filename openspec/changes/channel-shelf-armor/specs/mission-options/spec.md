## ADDED Requirements

### Requirement: armor strike target class
Mission options SHALL expose `strike_target_class` id `armor` with supported
Channel unit_ids including `Pz_IV_H`, `Stug_III`, `Cromwell_IV`, and
`M4_Sherman`, preferred_motion path, and preferred_ai_preset convoy_transit.

#### Scenario: Class shelf lists armor ids
- **WHEN** catalog sync loads planning options
- **THEN** strike_target_class armor meta unit_ids MUST include Pz_IV_H,
  Stug_III, Cromwell_IV, and M4_Sherman
