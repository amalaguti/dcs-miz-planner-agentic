## ADDED Requirements

### Requirement: artillery strike target class
Mission options SHALL expose `strike_target_class` id `artillery` with supported
Channel unit_ids including `LeFH_18-40-105`, `Wespe124`, and `M2A1-105`,
preferred_motion static, and preferred_ai_preset convoy_transit.

#### Scenario: Class shelf lists artillery ids
- **WHEN** catalog sync loads planning options
- **THEN** strike_target_class artillery meta unit_ids MUST include
  LeFH_18-40-105, Wespe124, and M2A1-105

### Requirement: Channel extra invent homes
Mission options SHALL expose `channel_place` ids `hawkinge_home`, `detling_home`,
and `biggin_hill_home` with per-home geometry that MUST NOT copy Manston 135/25
or 125/76.

#### Scenario: Hawkinge home is not Manston geometry
- **WHEN** catalog/registry loads `hawkinge_home`
- **THEN** meta airfield MUST be Hawkinge and cap_bearing_deg MUST be 76

### Requirement: Normandy extra invent homes
Mission options SHALL expose `chailey_home`, `tangmere_home`, and `ford_af_home`.
Tangmere MUST publish `max_flight_size` 3.

#### Scenario: Tangmere parking cap is three
- **WHEN** catalog/registry loads `tangmere_home`
- **THEN** meta max_flight_size MUST be 3
