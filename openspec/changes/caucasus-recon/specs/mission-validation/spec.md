## ADDED Requirements

### Requirement: Caucasus recon Specs validate
Shared validation SHALL accept a well-formed Caucasus recon Spec
(theatre `Caucasus`, airfield `Batumi`, nested recon + land contacts)
when inventory agrees.

#### Scenario: Batumi recon validates
- **WHEN** `examples/batumi_kutaisi_recon.yaml` is validated against
  an inventory that includes offerable Caucasus
- **THEN** validation MUST succeed
