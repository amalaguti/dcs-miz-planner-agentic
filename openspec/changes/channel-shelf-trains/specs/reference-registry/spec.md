## ADDED Requirements

### Requirement: Channel trains shelf
Packaged Channel registry SHALL include land-domain train ids `Locomotive`,
`German_covered_wagon_G10`, `German_tank_wagon`, and `DR_50Ton_Flat_Wagon`, each
resolvable as a strike unit.

#### Scenario: Locomotive resolvable
- **WHEN** the registry is queried for Locomotive
- **THEN** it MUST return a land-domain strike unit

#### Scenario: German_covered_wagon_G10 resolvable
- **WHEN** the registry is queried for German_covered_wagon_G10
- **THEN** it MUST return a land-domain strike unit
