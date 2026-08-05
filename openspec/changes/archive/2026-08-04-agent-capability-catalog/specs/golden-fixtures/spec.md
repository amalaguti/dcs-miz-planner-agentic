## ADDED Requirements

### Requirement: Mission behaviour and inspiration options are covered
Tests MUST assert that after catalog sync (or registry load), packaged
`mission_behaviour` planning options include the v1 altitude/speed gate card, packaged
`mission_inspiration` includes at least one pattern card, and `list_mission_options`
exposes both families. Prompt or schema-note tests MAY assert that agent guidance mentions
`mission_behaviour` and inspiration/research/local-campaign creativity aids. Tests MUST
cover the local campaign index against a hermetic fixture tree.

#### Scenario: Behaviour options present in tool output
- **WHEN** tests call `list_mission_options` after sync
- **THEN** the result MUST include a `mission_behaviour` option for altitude/speed gates

#### Scenario: Inspiration options present in tool output
- **WHEN** tests call `list_mission_options` after sync
- **THEN** the result MUST include at least one `mission_inspiration` option

#### Scenario: Local campaign index fixture
- **WHEN** tests call the installed-campaigns tool against a fixture campaigns tree
- **THEN** the result MUST list the fixture campaign, at least one mission filename, and
  Doc filename(s) when the fixture includes a `Doc/` folder
