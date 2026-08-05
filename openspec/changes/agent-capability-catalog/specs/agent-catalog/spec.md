## ADDED Requirements

### Requirement: Catalog exposes mission behaviour and inspiration options
After catalog sync from packaged Channel data, planning-option queries MUST include
`mission_behaviour` and `mission_inspiration` family rows when present in the packaged
planning-options source, with the same support-level honesty as other planning options.

#### Scenario: Sync surfaces mission_behaviour
- **WHEN** catalog sync runs after packaged `mission_behaviour` options are added
- **THEN** listing planning options for family `mission_behaviour` MUST return those rows

#### Scenario: Sync surfaces mission_inspiration
- **WHEN** catalog sync runs after packaged `mission_inspiration` options are added
- **THEN** listing planning options for family `mission_inspiration` MUST return those rows
