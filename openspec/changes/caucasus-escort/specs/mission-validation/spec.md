## ADDED Requirements

### Requirement: Caucasus escort Specs validate
Shared validation SHALL accept a well-formed Caucasus escort Spec
(theatre `Caucasus`, airfield `Batumi`, nested escort + package) when
inventory agrees. It MUST still reject Caucasus recon invent.

#### Scenario: Batumi escort validates
- **WHEN** `examples/batumi_black_sea_escort.yaml` is validated against an
  inventory that includes offerable Caucasus
- **THEN** validation MUST succeed
