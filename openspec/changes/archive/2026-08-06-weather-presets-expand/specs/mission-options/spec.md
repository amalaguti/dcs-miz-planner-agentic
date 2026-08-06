## ADDED Requirements

### Requirement: Planning options list expanded weather patterns
Packaged planning options for family `weather` MUST include the expanded pattern
ids as `supported` (or honestly labeled) with descriptions aligned to registry
weather descriptions after catalog sync.

#### Scenario: Expanded weather listable
- **WHEN** `list_mission_options` runs after catalog sync
- **THEN** results MUST include the new weather pattern ids as well as the
  original trio
