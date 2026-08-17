## ADDED Requirements

### Requirement: Caucasus CAP Specs validate
Shared validation SHALL accept a well-formed Caucasus CAP Spec (theatre
`Caucasus`, airfield `Batumi`, CAP geometry present, player Georgia `Su-25T`,
enemies Russia `Su-25T` red) when inventory agrees. It MUST still reject
Caucasus intercept with `intercept_unsupported_theatre` and Caucasus
strike/recon/path geometry with `domain_unsupported_theatre`.

#### Scenario: Batumi CAP validates
- **WHEN** `examples/batumi_black_sea_cap.yaml` is validated against an
  inventory that includes offerable Caucasus
- **THEN** validation MUST succeed

#### Scenario: Caucasus intercept still fails closed
- **WHEN** a Mission Spec sets theatre `Caucasus` and `mission_type: intercept`
- **THEN** validation MUST fail with `intercept_unsupported_theatre`
