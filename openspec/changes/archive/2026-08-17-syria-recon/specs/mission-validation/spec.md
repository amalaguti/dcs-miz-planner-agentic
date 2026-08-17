## ADDED Requirements

### Requirement: Syria recon Specs validate
Shared validation SHALL accept a well-formed Syria recon Spec
(theatre `Syria`, airfield `Incirlik`, nested recon + land observe targets)
when inventory agrees.

#### Scenario: Incirlik Aleppo recon validates
- **WHEN** `examples/incirlik_aleppo_recon.yaml` is validated against an
  inventory that includes offerable Syria
- **THEN** validation MUST succeed
