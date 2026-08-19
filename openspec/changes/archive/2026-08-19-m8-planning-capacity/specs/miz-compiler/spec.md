## ADDED Requirements

### Requirement: Compile scenery statics
The compiler SHALL place validated `scenery[]` entries as PyDCS static groups
via `fortification_map` keys, airfield-relative from the player airport.

#### Scenario: Manston scenery compiles
- **WHEN** `examples/manston_freeflight_scenery.yaml` is compiled
- **THEN** the `.miz` MUST include static groups for the listed types
