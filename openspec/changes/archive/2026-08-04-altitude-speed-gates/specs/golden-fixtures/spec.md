## ADDED Requirements

### Requirement: Altitude and speed gate example is covered
The repository MUST include a checked-in Spec that uses at least one of
`unit_altitude_higher`, `unit_altitude_lower`, `unit_speed_higher`, or
`unit_speed_lower`, with at least one observable companion action (e.g. `message`).
Tests MUST assert validation and compile emit of the corresponding unit-altitude and/or
unit-speed predicates for the player unit.

#### Scenario: Gate compile structure
- **WHEN** the altitude/speed gate example is compiled in tests
- **THEN** the resulting `.miz` MUST include unit-altitude and/or unit-speed predicates
  consistent with the Spec
