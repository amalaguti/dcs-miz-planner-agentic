## ADDED Requirements

### Requirement: Catalog lists radar_c3 strike units
After catalog sync, `list_strike_targets` with class_id `radar_c3` SHALL return
the promoted Channel radar unit ids.

#### Scenario: Filter by radar_c3
- **WHEN** list_strike_targets is called with class_id radar_c3
- **THEN** the result MUST include FuMG-401 among unit_ids
