## ADDED Requirements

### Requirement: Planning options list showers scattered
Packaged planning options for family `weather` MUST include
`showers_scattered` as `supported` with a description aligned to the registry
weather description after catalog sync.

#### Scenario: Showers listable
- **WHEN** `list_mission_options` runs after catalog sync
- **THEN** weather results MUST include `showers_scattered` as `supported`
