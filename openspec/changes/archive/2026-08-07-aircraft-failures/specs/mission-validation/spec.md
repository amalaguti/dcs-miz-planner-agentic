## ADDED Requirements

### Requirement: Aircraft failure validation
Shared validation SHALL reject unknown failure ids for the player aircraft, out-of-
range probability / times, and MUST NOT invent DCS failure strings. When `failures`
is non-empty and the player aircraft has no failure catalog, validation MUST fail
clearly.

#### Scenario: Unknown id rejected
- **WHEN** a Spec sets `failures[].id` to a string not in the Channel catalog for
  `player.aircraft`
- **THEN** validation MUST fail with a clear unknown-failure error

#### Scenario: Probability out of range rejected
- **WHEN** `failures[].probability` is outside 0–100
- **THEN** load or validation MUST fail
