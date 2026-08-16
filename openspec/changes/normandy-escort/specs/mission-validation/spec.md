## ADDED Requirements

### Requirement: Normandy escort Specs validate
Shared validation SHALL accept a well-formed Normandy escort Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, nested escort + package)
when inventory agrees. It MUST still reject Normandy recon invent.

#### Scenario: Needs Oar Point escort validates
- **WHEN** `examples/needs_oar_point_escort.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed
