## ADDED Requirements

### Requirement: Catalog lists R13 leftover strike units
After catalog sync, list_strike_targets SHALL return leftover ids under the
correct class filters.

#### Scenario: Artillery filter includes v1_launcher
- **WHEN** list_strike_targets is called with class_id artillery
- **THEN** results MUST include v1_launcher
