## ADDED Requirements

### Requirement: Channel R13 leftover land units
Packaged Channel registry SHALL include leftover campaign land ids
`v1_launcher`, `SK_C_28_naval_gun`, `Coach a tank yellow`,
`Coach a tank blue`, and `Coach a platform`.

#### Scenario: v1_launcher resolvable
- **WHEN** the registry is queried for v1_launcher
- **THEN** it MUST return a land-domain strike unit

#### Scenario: Coach a tank yellow resolvable
- **WHEN** the registry is queried for Coach a tank yellow
- **THEN** it MUST return a land-domain strike unit
