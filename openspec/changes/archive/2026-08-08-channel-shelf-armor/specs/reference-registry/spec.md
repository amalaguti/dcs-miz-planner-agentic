## ADDED Requirements

### Requirement: Channel armor shelf
Packaged Channel registry SHALL include land-domain armor ids `Pz_IV_H`,
`Stug_III`, `Cromwell_IV`, and `M4_Sherman`, each resolvable as a strike unit.

#### Scenario: Pz_IV_H resolvable
- **WHEN** the registry is queried for Pz_IV_H
- **THEN** it MUST return a land-domain strike unit

#### Scenario: Stug_III resolvable
- **WHEN** the registry is queried for Stug_III
- **THEN** it MUST return a land-domain strike unit
