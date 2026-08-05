## ADDED Requirements

### Requirement: Creative decision memory is hermetically tested
Tests MUST cover recording generation detail with a `creative` object and the bias
helper’s prefer/avoid behaviour on fixture history/feedback without a live LLM or DCS
install.

#### Scenario: Detail round-trip in tests
- **WHEN** tests record a generation with creative behaviours in detail
- **THEN** listed history MUST include those behaviours

#### Scenario: Bias helper unit test
- **WHEN** tests feed a high-scored generation with known behaviours into the bias helper
- **THEN** prefer MUST be non-empty for those behaviours
