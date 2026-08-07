## ADDED Requirements

### Requirement: Recon golden fixture
The test suite SHALL include a structural golden (or compile asserts) for a checked-in
recon example that verifies Reconnaissance task presence, AOI zone, absence of bomb
CLSIDs, and find-beat messaging/trigger text. Contact unit types MUST be asserted when the
example includes `targets`.

#### Scenario: Recon golden green
- **WHEN** the recon golden / compile test runs in CI
- **THEN** it MUST pass against the checked-in example Spec
