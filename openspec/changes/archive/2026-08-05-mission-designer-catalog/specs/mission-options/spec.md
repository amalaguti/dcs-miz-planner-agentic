## ADDED Requirements

### Requirement: Mission-designer shelf families in planning options
The packaged planning-option catalog SHALL include families `dynamics_mode`,
`strike_target_class`, and `channel_place` for mission-designer co-authoring. Entries
MUST use support `supported`, `advisory`, or `future` honestly. `dynamics_mode` rows
MUST remain non-`supported` until a later change makes Spec dynamics compile-backed.
`strike_target_class` meta MUST NOT invent DCS unit/ship ids (only ids present in
packaged Channel ground/ship YAML). `channel_place` MUST NOT invent airdromeIds.

#### Scenario: Dynamics modes packaged
- **WHEN** catalog sync runs after this change
- **THEN** listing planning options for family `dynamics_mode` MUST include ids
  `fixed`, `live`, `choose`, and `hybrid`

#### Scenario: Strike target classes packaged
- **WHEN** a caller lists planning options for family `strike_target_class`
- **THEN** results MUST include at least one land-domain class and one sea-domain class
  with meta that names domain and verified unit or ship ids where applicable

#### Scenario: Channel places packaged
- **WHEN** a caller lists planning options for family `channel_place`
- **THEN** results MUST include at least one place referencing Manston or another known
  Channel airfield without inventing airdrome ids
