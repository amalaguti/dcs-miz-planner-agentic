## ADDED Requirements

### Requirement: Dynamics expand validation
Validation MUST expand `dynamics` (when present) before or as part of graph checks, and
MUST verify pool indices, late_activation on referenced groups, roll range, and mode
field consistency. Invalid dynamics MUST produce structured errors (not silent omit).

#### Scenario: Missing late_activation on pooled enemy
- **WHEN** a pool references an enemy without late_activation and mode requires dormant
  pools
- **THEN** validation MUST fail or the expander MUST set late_activation true before
  emit — product MUST pick one behaviour and document it; v1 lean fail-closed if unset

#### Scenario: Bad enemy index
- **WHEN** `enemy_indices` contains an out-of-range index
- **THEN** validation MUST fail with path pointing at the pool
