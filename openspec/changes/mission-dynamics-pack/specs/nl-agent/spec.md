## ADDED Requirements

### Requirement: Schema and invent guidance mention dynamics Spec
`get_mission_spec_schema` notes and invent/chat guidance MUST mention optional Spec
`dynamics` (modes + pools) as the preferred way to declare play-time live/choose/hybrid
variation, distinct from CLI `randomize`. Guidance MUST still require co-author consult of
catalog `dynamics_mode` shelves and MUST NOT invent Lua.

#### Scenario: Prompt mentions dynamics Spec field
- **WHEN** the planning system prompt is built
- **THEN** it MUST mention Spec `dynamics` (or equivalent) for play-time variation

#### Scenario: Schema notes mention dynamics
- **WHEN** `get_mission_spec_schema` is requested for a combat mission type
- **THEN** notes MUST reference optional `dynamics` expand without claiming Mist
