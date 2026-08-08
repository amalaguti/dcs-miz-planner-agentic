## ADDED Requirements

### Requirement: Catalog lists troops strike units
After catalog sync, `list_strike_targets` with class_id `troops` SHALL return the
promoted Channel infantry unit ids.

#### Scenario: Filter by troops
- **WHEN** list_strike_targets is called with class_id troops
- **THEN** the result MUST include soldier_mauser98 among unit_ids
