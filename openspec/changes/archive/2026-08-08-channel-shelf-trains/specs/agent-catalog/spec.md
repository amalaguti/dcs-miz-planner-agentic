## ADDED Requirements

### Requirement: Catalog lists trains strike units
After catalog sync, `list_strike_targets` with class_id `trains` SHALL return the
promoted Channel train unit ids.

#### Scenario: Filter by trains
- **WHEN** list_strike_targets is called with class_id trains
- **THEN** the result MUST include Locomotive among unit_ids
