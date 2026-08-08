## ADDED Requirements

### Requirement: Class shelves list R13 promoted units
Mission options strike_target_class shelves SHALL list the R13-promoted unit and
ship ids on aaa_guns, armor, trains, and sea_craft respectively.

#### Scenario: AAA includes flak41
- **WHEN** catalog sync loads aaa_guns
- **THEN** unit_ids MUST include flak41 and M45_Quadmount

#### Scenario: Sea includes LST_Mk2
- **WHEN** catalog sync loads sea_craft
- **THEN** ship_ids MUST include LST_Mk2 and USS_Samuel_Chase
