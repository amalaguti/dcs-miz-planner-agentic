## ADDED Requirements

### Requirement: Channel troops shelf
Packaged Channel registry SHALL include land-domain infantry ids
`soldier_mauser98`, `soldier_wwii_br_01`, and `soldier_wwii_us`, each resolvable
as a strike unit.

#### Scenario: soldier_mauser98 resolvable
- **WHEN** the registry is queried for soldier_mauser98
- **THEN** it MUST return a land-domain strike unit

#### Scenario: soldier_wwii_br_01 resolvable
- **WHEN** the registry is queried for soldier_wwii_br_01
- **THEN** it MUST return a land-domain strike unit
