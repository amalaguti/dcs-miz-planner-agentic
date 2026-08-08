## ADDED Requirements

### Requirement: troops strike target class
Mission options SHALL expose `strike_target_class` id `troops` with supported
Channel unit_ids including `soldier_mauser98`, `soldier_wwii_br_01`, and
`soldier_wwii_us`, preferred_motion path, and preferred_ai_preset convoy_transit.

#### Scenario: Class shelf lists troops ids
- **WHEN** catalog sync loads planning options
- **THEN** strike_target_class troops meta unit_ids MUST include
  soldier_mauser98, soldier_wwii_br_01, and soldier_wwii_us
