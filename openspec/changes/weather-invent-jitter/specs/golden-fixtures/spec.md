## ADDED Requirements

### Requirement: Weather invent tests pin seeds
Hermetic weather invent / compile tests that assert exact weather emit MUST set
an explicit `weather_opts.seed`. SoT parity for pattern ids MUST remain green
when invent metadata (gallery families) is added.

#### Scenario: Invent determinism test
- **WHEN** the weather invent test suite runs
- **THEN** at least one test MUST prove same seed → same snapshot and different
  seeds → differing within-family result for a gallery pattern
