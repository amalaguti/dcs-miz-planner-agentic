## ADDED Requirements

### Requirement: Escort mission type in planning options
The planning-options catalog SHALL list `mission_type` value `escort` as `supported`,
describing Channel escort / package-protection planning.

#### Scenario: escort listed as supported
- **WHEN** an agent or CLI lists mission-type planning options
- **THEN** `escort` MUST appear with status `supported`
