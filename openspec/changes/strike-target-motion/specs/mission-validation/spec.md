## ADDED Requirements

### Requirement: Validate target motion and domain
Validation MUST reject invalid motion combinations (patrol without radius, path
without enough points, mixed patrol+path fields, out-of-range radius). Path
waypoints and patrol centers MUST be checked against the unit’s land|sea domain
using the same Channel domain rules as strike/recon placement. Domain mismatches
MUST fail validation.

#### Scenario: Sea path on land rejected
- **WHEN** a sea-domain unit has a path point classified as land
- **THEN** validation MUST fail with a domain mismatch error

#### Scenario: Land truck path on land accepted
- **WHEN** a land soft-vehicle target has a short inland path
- **THEN** validation MUST succeed
