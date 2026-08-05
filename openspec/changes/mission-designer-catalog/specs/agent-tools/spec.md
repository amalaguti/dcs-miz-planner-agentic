## ADDED Requirements

### Requirement: list_mission_options surfaces mission-designer shelves
`list_mission_options` MUST return packaged `dynamics_mode`, `strike_target_class`, and
`channel_place` planning options (family, id, description, support, meta) after catalog
sync so agents can co-author recommendations from declared shelves. The tool description
MUST mention these designer shelves (not only envelope enums and behaviour cards).

#### Scenario: Tool returns dynamics_mode rows
- **WHEN** `list_mission_options` is called after catalog sync with dynamics modes packaged
- **THEN** the enriched options collection MUST include `dynamics_mode` rows for
  `fixed`, `live`, `choose`, and `hybrid`

#### Scenario: Tool returns strike_target_class rows
- **WHEN** `list_mission_options` is called after catalog sync with strike classes packaged
- **THEN** the enriched options collection MUST include at least one
  `strike_target_class` row whose meta includes `domain`

#### Scenario: Tool returns channel_place rows
- **WHEN** `list_mission_options` is called after catalog sync with places packaged
- **THEN** the enriched options collection MUST include at least one `channel_place` row
