## ADDED Requirements

### Requirement: Strike class shelves list expanded Channel units
`strike_target_class` soft_vehicles, aaa_guns, and sea_craft planning options
SHALL list the newly promoted Channel unit/ship ids in meta after packaging.

#### Scenario: Soft class includes Kettenkrad
- **WHEN** catalog sync loads soft_vehicles
- **THEN** unit_ids MUST include Sd_Kfz_2

#### Scenario: AAA class includes flak38
- **WHEN** catalog sync loads aaa_guns
- **THEN** unit_ids MUST include flak38

#### Scenario: Sea class includes HarborTug
- **WHEN** catalog sync loads sea_craft
- **THEN** ship_ids MUST include HarborTug
