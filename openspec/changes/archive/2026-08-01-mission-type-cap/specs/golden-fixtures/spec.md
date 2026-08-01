## ADDED Requirements

### Requirement: CAP structural golden
The repository SHALL include a golden-fixture regression for the checked-in Manston CAP
compile path (injected Channel inventory), covering required zip members and contracted
mission content for player CAP tasking (Orbit / engagement) and any example enemies.
Ordinary pytest MUST NOT rewrite those fixtures; refresh MUST be explicit.

#### Scenario: CAP compile matches golden
- **WHEN** the CAP example Spec is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the CAP golden contracts
  (including Spitfire presence, CAP/Orbit-related contracts, and engagement/ROE as designed)
