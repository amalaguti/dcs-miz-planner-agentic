## ADDED Requirements

### Requirement: Catalog lists R13 promoted strike units
After catalog sync, list_strike_targets SHALL return R13-promoted ids under the
correct class filters.

#### Scenario: Armor filter includes Tiger_I
- **WHEN** list_strike_targets is called with class_id armor
- **THEN** results MUST include Tiger_I
