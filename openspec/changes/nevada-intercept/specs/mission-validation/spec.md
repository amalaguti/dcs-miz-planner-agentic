## ADDED Requirements

### Requirement: Nevada intercept Specs validate
Shared validation SHALL accept a well-formed Nevada intercept Spec
(theatre `Nevada`, airfield `Nellis`) when inventory agrees. Well-formed
Nevada intercept Specs MUST NOT fail solely with
`intercept_unsupported_theatre`. Falklands MUST still fail closed.

#### Scenario: Nellis intercept validates
- **WHEN** `examples/nellis_dawn_intercept.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed
