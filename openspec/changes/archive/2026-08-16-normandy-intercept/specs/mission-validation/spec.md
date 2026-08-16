## ADDED Requirements

### Requirement: Normandy intercept Specs validate
Shared validation SHALL accept a well-formed Normandy intercept Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, enemies present) when
inventory agrees. It MUST still reject Normandy escort/recon invent, but
MUST NOT fail Normandy intercept solely with `intercept_unsupported_theatre`.

#### Scenario: Needs Oar Point intercept validates
- **WHEN** `examples/needs_oar_point_dawn_intercept.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed

## MODIFIED Requirements

### Requirement: Intercept spawn is Channel-only
Validation SHALL reject `mission_type: intercept` when Spec theatre is not
`TheChannel` or `Normandy`, with stable code `intercept_unsupported_theatre`
(or equivalent).

#### Scenario: Caucasus intercept fails validation
- **WHEN** a Mission Spec sets theatre `Caucasus` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`
