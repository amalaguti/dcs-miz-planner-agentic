## ADDED Requirements

### Requirement: Escort schema via get_mission_spec_schema
The `get_mission_spec_schema` agent tool SHALL support `mission_type` `escort`, returning a
derived example shape consistent with the checked-in escort example (nested `escort`,
`package`, optional `enemies`, `escort_package` objective).

#### Scenario: Escort schema example validates
- **WHEN** an agent or test requests `get_mission_spec_schema` for `escort`
- **THEN** the returned example MUST load as a structurally valid escort Mission Spec
  (subject to registry checks)
