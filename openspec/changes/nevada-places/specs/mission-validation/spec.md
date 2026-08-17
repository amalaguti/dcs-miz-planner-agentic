## ADDED Requirements

### Requirement: Nevada CAP Specs validate
Shared validation SHALL accept a well-formed Nevada CAP Spec
(theatre `Nevada`, airfield `Nellis`, nested cap) when inventory agrees.
It MUST still reject Nevada intercept invent.

#### Scenario: Nellis CAP validates
- **WHEN** `examples/nellis_north_range_cap.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed
