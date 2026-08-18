## ADDED Requirements

### Requirement: Nevada recon Specs validate
Shared validation SHALL accept a well-formed Nevada recon Spec
(theatre `Nevada`, airfield `Nellis`, nested recon + land observe targets)
when inventory agrees.

#### Scenario: Nellis Creech recon validates
- **WHEN** `examples/nellis_creech_recon.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed
