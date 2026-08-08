## ADDED Requirements

### Requirement: Channel halftracks_apc shelf
Packaged Channel registry SHALL include land-domain halftrack ids `Sd_Kfz_251`,
`Sd_Kfz_7`, and `M2A1_halftrack`, each resolvable as a strike unit.

#### Scenario: Sd_Kfz_251 resolvable
- **WHEN** the registry is queried for Sd_Kfz_251
- **THEN** it MUST return a land-domain strike unit

#### Scenario: M2A1_halftrack resolvable
- **WHEN** the registry is queried for M2A1_halftrack
- **THEN** it MUST return a land-domain strike unit
