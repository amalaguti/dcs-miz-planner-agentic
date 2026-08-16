## ADDED Requirements

### Requirement: Channel rejects Turkey
Shared validation SHALL reject player country `Turkey` on a WWII theatre
(TheChannel / Normandy) with an unknown-country error. A Syria Spec MAY
use `Turkey`.

#### Scenario: Channel rejects Turkey
- **WHEN** a TheChannel Mission Spec sets player country `Turkey`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Syria freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Syria`
and airfield `Incirlik` when the packaged registry supports Syria, a terrain
binding exists, and the install inventory reports `Syria` as available and
planner-supported.

#### Scenario: Valid Incirlik freeflight passes
- **WHEN** the checked-in Syria cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Syria` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Syria rejects Spitfire
- **WHEN** a Syria Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST fail with an unknown-aircraft error
