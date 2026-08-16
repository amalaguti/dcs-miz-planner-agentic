## ADDED Requirements

### Requirement: Falklands freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Falklands`
and airfield `MountPleasant` when the packaged registry supports Falklands, a
terrain binding exists, and the install inventory reports `Falklands` as
available and planner-supported.

#### Scenario: Valid Mount Pleasant freeflight passes
- **WHEN** the checked-in Falklands cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Falklands` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Falklands rejects Spitfire
- **WHEN** a Falklands Mission Spec sets player aircraft `SpitfireLFMkIX`
- **THEN** validation MUST fail with an unknown-aircraft error

#### Scenario: Channel still accepts UK
- **WHEN** a TheChannel Mission Spec sets player country `UK`
- **THEN** validation MUST succeed for country (WWII era still includes UK)
