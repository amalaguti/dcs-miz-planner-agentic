## ADDED Requirements

### Requirement: Channel rejects USA
Shared validation SHALL reject player country `USA` on a WWII theatre
(TheChannel / Normandy) with an unknown-country error. A Nevada Spec MAY
use `USA`.

#### Scenario: Channel rejects USA
- **WHEN** a TheChannel Mission Spec sets player country `USA`
- **THEN** validation MUST fail with an unknown-country error

### Requirement: Nevada freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Nevada`
and airfield `Nellis` when the packaged registry supports Nevada, a terrain
binding exists, and the install inventory reports `Nevada` as available and
planner-supported.

#### Scenario: Valid Nellis freeflight passes
- **WHEN** the checked-in Nevada cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Nevada` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Nevada rejects Spitfire
- **WHEN** a Nevada Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST fail with an unknown-aircraft error
