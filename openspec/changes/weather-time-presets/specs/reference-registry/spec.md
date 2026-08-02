## ADDED Requirements

### Requirement: Channel registry lists dawn and marginal weather
The Channel reference registry SHALL expose weather preset ids `dawn_clear` and
`marginal_vfr` (in addition to `sunny_clear`) from packaged YAML, with descriptions
suitable for catalog/agent listing.

#### Scenario: Registry lists new presets
- **WHEN** a caller lists Channel weather presets
- **THEN** the result MUST include `sunny_clear`, `dawn_clear`, and `marginal_vfr`
