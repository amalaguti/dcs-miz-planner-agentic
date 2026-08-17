## ADDED Requirements

### Requirement: Nevada escort Specs validate
Shared validation SHALL accept a well-formed Nevada escort Spec
(theatre `Nevada`, airfield `Nellis`, nested escort + package) when
inventory agrees. It MUST still reject Nevada ground_attack invent.

#### Scenario: Nellis escort validates
- **WHEN** `examples/nellis_north_range_escort.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed
