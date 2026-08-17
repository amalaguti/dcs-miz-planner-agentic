## ADDED Requirements

### Requirement: Caucasus intercept Specs validate
Shared validation SHALL accept a well-formed Caucasus intercept Spec
(theatre `Caucasus`, airfield `Batumi`, enemies present) when inventory
agrees. It MUST NOT fail Caucasus intercept solely with
`intercept_unsupported_theatre`. It MUST still reject Caucasus escort/recon
invent.

#### Scenario: Batumi intercept validates
- **WHEN** `examples/batumi_dawn_intercept.yaml` is validated against an
  inventory that includes offerable Caucasus
- **THEN** validation MUST succeed

## MODIFIED Requirements

### Requirement: Intercept spawn is Channel-only
Validation SHALL reject `mission_type: intercept` when Spec theatre is not
`TheChannel`, `Normandy`, or `Caucasus`, with stable code
`intercept_unsupported_theatre` (or equivalent).

#### Scenario: Syria intercept fails validation
- **WHEN** a Mission Spec sets theatre `Syria` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`
