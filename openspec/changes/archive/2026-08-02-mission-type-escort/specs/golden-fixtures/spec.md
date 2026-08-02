## ADDED Requirements

### Requirement: Escort golden fixture
The test suite SHALL include a hermetic golden fixture for the Manston escort example that
asserts required `.miz` zip members and structural mission contracts for Escort tasking,
friendly package aircraft presence, and player placement/frequency — without requiring a
live DCS install at test time.

#### Scenario: Escort golden regresses structure
- **WHEN** the Manston escort example is compiled in tests and compared to its golden
  fixture
- **THEN** required members and escort structural contracts MUST match (allowing documented
  volatile fields such as onboard numbers)
