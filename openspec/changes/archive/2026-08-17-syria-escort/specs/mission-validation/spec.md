## ADDED Requirements

### Requirement: Syria escort Specs validate
Shared validation SHALL accept a well-formed Syria escort Spec
(theatre `Syria`, airfield `Incirlik`, nested escort + package) when
inventory agrees. It MUST still reject Syria ground_attack invent.

#### Scenario: Incirlik escort validates
- **WHEN** `examples/incirlik_iskenderun_escort.yaml` is validated against an
  inventory that includes offerable Syria
- **THEN** validation MUST succeed
