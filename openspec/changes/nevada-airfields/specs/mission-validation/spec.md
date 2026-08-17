## ADDED Requirements

### Requirement: Extra Nevada airfields validate
Shared validation SHALL accept a well-formed Nevada free-flight Spec whose
player airfield is a curated extra Nevada key (e.g. `GroomLake`) when
inventory agrees. Combat invent on Nevada MUST still be rejected.

#### Scenario: Groom Lake freeflight validates
- **WHEN** `examples/groom_lake_cold_freeflight.yaml` is validated against an
  inventory that includes offerable Nevada
- **THEN** validation MUST succeed
