## ADDED Requirements

### Requirement: Normandy recon Specs validate
Shared validation SHALL accept a well-formed Normandy recon Spec
(theatre `Normandy`, airfield `NeedsOarPoint`, nested recon + land contacts)
when inventory agrees.

#### Scenario: Needs Oar Point recon validates
- **WHEN** `examples/needs_oar_point_recon.yaml` is validated against
  an inventory that includes offerable Normandy
- **THEN** validation MUST succeed
