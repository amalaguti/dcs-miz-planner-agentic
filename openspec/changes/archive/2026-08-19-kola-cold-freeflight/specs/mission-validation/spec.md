## ADDED Requirements

### Requirement: Kola freeflight validates when inventory agrees
Validation SHALL accept a free-flight Mission Spec with theatre `Kola` and
airfield `Bodo` when the packaged registry supports Kola, a terrain binding
exists, and the install inventory reports `Kola` as available and
planner-supported.

#### Scenario: Valid Bodo freeflight passes
- **WHEN** the checked-in Kola cold freeflight Mission Spec is validated
  against the registry and an inventory that reports `Kola` available and
  planner-supported
- **THEN** the validation result MUST indicate success with no errors

#### Scenario: Channel rejects Norway
- **WHEN** a TheChannel Mission Spec sets player country `Norway`
- **THEN** validation MUST fail with an unknown-country error

#### Scenario: Channel still accepts UK
- **WHEN** a TheChannel Mission Spec sets player country `UK`
- **THEN** validation MUST succeed for country (WWII era still includes UK)
