## ADDED Requirements

### Requirement: halftracks_apc strike target class
Mission options SHALL expose `strike_target_class` id `halftracks_apc` with
supported Channel unit_ids including `Sd_Kfz_251`, `Sd_Kfz_7`, and
`M2A1_halftrack`, preferred_motion path, and preferred_ai_preset convoy_transit.

#### Scenario: Class shelf lists halftrack ids
- **WHEN** catalog sync loads planning options
- **THEN** strike_target_class halftracks_apc meta unit_ids MUST include
  Sd_Kfz_251, Sd_Kfz_7, and M2A1_halftrack
