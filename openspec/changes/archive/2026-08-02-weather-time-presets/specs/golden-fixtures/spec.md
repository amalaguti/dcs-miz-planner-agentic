## ADDED Requirements

### Requirement: Non-sunny weather covered by regression
The test suite SHALL regress compile output for at least one non-`sunny_clear` weather
example (dawn and/or marginal VFR) via golden fixtures or equivalent structural contracts
so weather mappings cannot silently regress.

#### Scenario: Dawn or marginal golden/contract
- **WHEN** the dawn or marginal VFR example is compiled under the test harness
- **THEN** the suite MUST assert required members and weather-related contracts (or full
  golden match) for that example
