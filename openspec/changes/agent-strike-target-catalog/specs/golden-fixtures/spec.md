## ADDED Requirements

### Requirement: Strike unit catalog covered by tests
Hermetic tests SHALL assert that catalog sync populates strike units and that
`list_strike_targets` filters work offline without a live DCS install.

#### Scenario: Catalog strike unit tests green
- **WHEN** catalog / tool tests run in CI
- **THEN** they MUST pass and fail if Uboat sea membership or tool filters regress
