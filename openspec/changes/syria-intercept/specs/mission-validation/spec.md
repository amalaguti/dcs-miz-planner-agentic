## ADDED Requirements

### Requirement: Syria intercept Specs validate
Shared validation SHALL accept a well-formed Syria intercept Spec
(theatre `Syria`, airfield `Incirlik`) when inventory agrees. Well-formed
Syria intercept Specs MUST NOT fail solely with
`intercept_unsupported_theatre`. Nevada MUST still fail closed.

#### Scenario: Incirlik intercept validates
- **WHEN** `examples/incirlik_dawn_intercept.yaml` is validated against an
  inventory that includes offerable Syria
- **THEN** validation MUST succeed
