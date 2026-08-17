## ADDED Requirements

### Requirement: Syria CAP Specs validate
Shared validation SHALL accept a well-formed Syria CAP Spec
(theatre `Syria`, airfield `Incirlik`, nested cap) when inventory agrees.
It MUST still reject Syria intercept invent.

#### Scenario: Incirlik CAP validates
- **WHEN** `examples/incirlik_iskenderun_cap.yaml` is validated against an
  inventory that includes offerable Syria
- **THEN** validation MUST succeed
