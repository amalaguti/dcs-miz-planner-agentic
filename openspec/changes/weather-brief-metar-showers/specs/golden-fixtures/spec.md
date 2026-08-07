## ADDED Requirements

### Requirement: Showers example or METAR contract coverage
The test suite SHALL cover `showers_scattered` and synthetic METAR hermetically:
either a checked-in example Spec compiled under the harness with weather-table
and briefing-substring contracts, or focused unit/contract tests that assert
(1) invent/compile gallery id ∈ showers family and (2) brief METAR contains the
fixed station id and simulated marker. Ordinary pytest MUST NOT require network
meteo.

#### Scenario: Showers or METAR contract passes offline
- **WHEN** the showers / METAR contract tests run in CI
- **THEN** they MUST pass without live METAR APIs and MUST fail if the gallery
  family or METAR markers regress
