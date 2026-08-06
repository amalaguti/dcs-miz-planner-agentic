## ADDED Requirements

### Requirement: Catalog exposes mission-designer shelf options
After catalog sync from packaged Channel data, planning-option queries MUST include
`dynamics_mode`, `strike_target_class`, and `channel_place` family rows when present in
the packaged planning-options source, with the same support-level honesty as other
planning options.

#### Scenario: Sync surfaces dynamics_mode
- **WHEN** catalog sync runs after packaged `dynamics_mode` options are added
- **THEN** listing planning options for family `dynamics_mode` MUST return those rows

#### Scenario: Sync surfaces strike_target_class
- **WHEN** catalog sync runs after packaged `strike_target_class` options are added
- **THEN** listing planning options for family `strike_target_class` MUST return those rows

#### Scenario: Sync surfaces channel_place
- **WHEN** catalog sync runs after packaged `channel_place` options are added
- **THEN** listing planning options for family `channel_place` MUST return those rows
