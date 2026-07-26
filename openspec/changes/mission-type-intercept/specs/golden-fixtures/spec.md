## ADDED Requirements

### Requirement: Intercept structural golden
The repository SHALL include a golden-fixture regression for the checked-in Manston intercept
compile path (injected Channel inventory), covering required zip members and contracted
mission content for player and enemy aircraft. Ordinary pytest MUST NOT rewrite those
fixtures; refresh MUST be explicit.

#### Scenario: Intercept compile matches golden
- **WHEN** the intercept example Spec is compiled under the golden harness
- **THEN** the test MUST pass if and only if output matches the intercept golden contracts
  (including `Bf-109K-4` and Spitfire presence)
