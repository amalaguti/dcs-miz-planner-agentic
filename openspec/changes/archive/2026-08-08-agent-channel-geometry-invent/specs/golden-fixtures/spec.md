## ADDED Requirements

### Requirement: Channel geometry invent covered by tests
Hermetic tests SHALL assert channel_place geometry recipes after catalog sync
and that domain-mismatch repair nudges include geometry guidance.

#### Scenario: Place recipe and repair tests green
- **WHEN** catalog / agent tests run in CI
- **THEN** they MUST pass and fail if inland/mid-Channel recipes or repair
  geometry text regress
