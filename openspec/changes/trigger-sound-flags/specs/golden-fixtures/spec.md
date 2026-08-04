## ADDED Requirements

### Requirement: Sound and numeric-flag example is covered
The repository MUST include a checked-in Spec that uses a `sound` action with a curated
`asset_id` and at least one numeric or timed flag rule (`flag_equals` / `flag_more` /
`flag_less` / `time_since_flag` and/or `inc_flag` / `set_flag_value`). Tests MUST assert
validation and compile emit sound-to-all (with embedded resource) and numeric flag
structure.

#### Scenario: Sound and flag compile structure
- **WHEN** the sound / numeric-flag example is compiled in tests
- **THEN** the resulting `.miz` MUST include sound-to-all and numeric flag markers
  consistent with the Spec
