## ADDED Requirements

### Requirement: Catalog lists armor strike units
After catalog sync, `list_strike_targets` with class_id `armor` SHALL return the
promoted Channel armor unit ids.

#### Scenario: Filter by armor
- **WHEN** list_strike_targets is called with class_id armor
- **THEN** the result MUST include Pz_IV_H among unit_ids
