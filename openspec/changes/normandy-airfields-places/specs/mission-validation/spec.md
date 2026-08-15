## ADDED Requirements

### Requirement: Normandy CAP Specs validate
Shared validation SHALL accept a well-formed Normandy CAP Spec (theatre
`Normandy`, airfield `NeedsOarPoint`, CAP geometry present) when inventory
agrees. It MUST still reject Normandy intercept with
`intercept_unsupported_theatre` and Normandy strike/recon/path geometry with
`domain_unsupported_theatre`.

#### Scenario: Needs Oar Point CAP validates
- **WHEN** `examples/needs_oar_point_cap.yaml` is validated against an
  inventory that includes offerable Normandy
- **THEN** validation MUST succeed

#### Scenario: Normandy intercept still fails closed
- **WHEN** a Mission Spec sets theatre `Normandy` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`
