## ADDED Requirements

### Requirement: radar_c3 strike target class
Mission options SHALL expose `strike_target_class` id `radar_c3` with supported
Channel unit_ids including `FuMG-401` and `FuSe-65`, preferred_motion static, and
preferred_ai_preset convoy_transit.

#### Scenario: Class shelf lists radar ids
- **WHEN** catalog sync loads planning options
- **THEN** strike_target_class radar_c3 meta unit_ids MUST include FuMG-401 and
  FuSe-65
