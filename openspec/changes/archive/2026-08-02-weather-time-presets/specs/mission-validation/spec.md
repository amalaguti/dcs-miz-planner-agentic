## ADDED Requirements

### Requirement: Unknown weather still rejected; new presets accepted
Shared validation SHALL accept registered weather presets `dawn_clear` and
`marginal_vfr` and MUST continue to reject unknown weather ids with a clear error listing
known presets.

#### Scenario: Unknown weather fails
- **WHEN** a Spec uses a weather value not in the Channel registry
- **THEN** validation MUST fail with an unknown-weather style error

#### Scenario: Dawn clear validates
- **WHEN** a Spec uses `weather: dawn_clear` on Channel with known player assets
- **THEN** validation MUST succeed for weather
