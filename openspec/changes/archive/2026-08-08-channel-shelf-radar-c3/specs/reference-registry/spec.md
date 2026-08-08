## ADDED Requirements

### Requirement: Channel radar_c3 shelf
Packaged Channel registry SHALL include land-domain radar ids `FuMG-401` and
`FuSe-65`, each resolvable as a strike unit.

#### Scenario: FuMG-401 resolvable
- **WHEN** the registry is queried for FuMG-401
- **THEN** it MUST return a land-domain strike unit

#### Scenario: FuSe-65 resolvable
- **WHEN** the registry is queried for FuSe-65
- **THEN** it MUST return a land-domain strike unit
