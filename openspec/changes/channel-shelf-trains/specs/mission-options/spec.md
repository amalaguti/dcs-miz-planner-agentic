## ADDED Requirements

### Requirement: trains strike target class
Mission options SHALL expose `strike_target_class` id `trains` with supported
Channel unit_ids including `Locomotive`, `German_covered_wagon_G10`,
`German_tank_wagon`, and `DR_50Ton_Flat_Wagon`, preferred_motion path, and
preferred_ai_preset convoy_transit.

#### Scenario: Class shelf lists train ids
- **WHEN** catalog sync loads planning options
- **THEN** strike_target_class trains meta unit_ids MUST include Locomotive and
  German_covered_wagon_G10

### Requirement: french_coast_rail_corridor place
Mission options SHALL expose `channel_place` id `french_coast_rail_corridor`
with land domain, related_classes including `trains`, strike geometry, and
non-empty path_point_deltas for invent to copy (not free-form rail routes).

#### Scenario: Rail corridor place lists trains
- **WHEN** catalog sync loads french_coast_rail_corridor
- **THEN** meta related_classes MUST include trains and path_point_deltas MUST
  be non-empty
