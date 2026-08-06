## ADDED Requirements

### Requirement: Fog dynamics validation
Shared validation MUST accept well-formed `fog_dynamics` and MUST reject invalid
timings (e.g. negative duration) with clear errors. Validation MUST NOT require
empty triggers solely because fog_dynamics is set.

#### Scenario: Negative duration rejected
- **WHEN** `fog_dynamics.duration_s` is negative
- **THEN** load or validation MUST fail
