## ADDED Requirements

### Requirement: Falklands CAP Specs validate
Shared validation SHALL accept a well-formed Falklands CAP Spec
(theatre `Falklands`, airfield `MountPleasant`, nested cap) when inventory
agrees. It MUST still reject Falklands intercept invent. Domain checks MUST
remain fail-closed on Falklands.

#### Scenario: Mount Pleasant CAP validates
- **WHEN** `examples/mount_pleasant_south_atlantic_cap.yaml` is validated
  against an inventory that includes offerable Falklands
- **THEN** validation MUST succeed
